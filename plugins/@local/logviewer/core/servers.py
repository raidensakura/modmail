from __future__ import annotations

import base64
import os
import re
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlparse

import aiohttp
import dateutil.parser
import discord
import jinja2
from aiohttp import web
from aiohttp.web import Application, Request, Response
from aiohttp_session import get_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from discord.utils import MISSING
from jinja2 import Environment, FileSystemLoader
from natural.date import duration

from core.models import getLogger

from .auth import authentication
from .handlers import AIOHTTPMethodHandler, aiohttp_error_handler
from .models import LogEntry, LogList

if TYPE_CHECKING:
    from jinja2 import Template  # noqa: F401

    from bot import ModmailBot

    from .types_ext import RawPayload


logger = getLogger(__name__)

# Set path for static
parent_dir = Path(__file__).parent.parent.resolve()
static_path = parent_dir / "static"

# Set path for templates
templates_path = parent_dir / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(templates_path),
    enable_async=True,
)

OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI = os.getenv("OAUTH2_REDIRECT_URI")

API_BASE = "https://discordapp.com/api/"
AUTHORIZATION_BASE_URL = f"{API_BASE}/oauth2/authorize"
TOKEN_URL = f"{API_BASE}/oauth2/token"
ROLE_URL = f"{API_BASE}/guilds/{{guild_id}}/members/{{user_id}}"


class Config:
    """
    Base class for storing configurations from `.env` (environment variables).
    """

    def __init__(self):
        self.log_prefix = os.getenv("URL_PREFIX", "/logs")
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8000))
        self.pagination = os.getenv("LOGVIEWER_PAGINATION", 25)

        self.using_oauth = all((OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_REDIRECT_URI))
        logger.info(f"Enabling Logviewer Oauth: {self.using_oauth}")
        if self.using_oauth:
            self.guild_id = os.getenv("GUILD_ID")
            self.bot_token = os.getenv("TOKEN")
            self.netloc = urlparse(OAUTH2_REDIRECT_URI).netloc
            self.bot_id = int(base64.b64decode(self.bot_token.split(".")[0] + "=="))


class LogviewerServer:
    """
    Main class to handle the log viewer server.
    """

    def __init__(self, bot: ModmailBot):
        self.bot: ModmailBot = bot
        self.config: Config = Config()

        self.app: Application = MISSING
        self.site: web.TCPSite = MISSING
        self.runner: web.AppRunner = MISSING
        self._hooked: bool = False
        self._running: bool = False

    def init_hook(self) -> None:
        """
        Initial setup to start the server.
        """
        self.app: Application = Application()
        self.app.router.add_static("/static", static_path)
        self.app["server"] = self

        self._add_routes()

        # middlewares
        self.app.middlewares.append(aiohttp_error_handler)

        self._hooked = True

        fernet_key = fernet.Fernet.generate_key()
        f = fernet.Fernet(fernet_key)
        setup(self.app, EncryptedCookieStorage(f))

    def _add_routes(self) -> None:
        prefix = self.config.log_prefix or "/logs"
        prefix.strip("/")
        self.app.router.add_route("HEAD", "/", AIOHTTPMethodHandler)
        self.app.router.add_route("GET", "/login{r:[\/]{0,1}}", AIOHTTPMethodHandler)
        self.app.router.add_route("GET", "/callback{r:[\/]{0,1}}", AIOHTTPMethodHandler)
        self.app.router.add_route("GET", "/logout{r:[\/]{0,1}}", AIOHTTPMethodHandler)
        self.app.router.add_route("GET", "/{prefix}{r:[\/]{0,1}}", AIOHTTPMethodHandler)
        for path in ("/", prefix + "/{key}{r:[\/]{0,1}}", prefix + "/raw/{key}{r:[\/]{0,1}}"):
            self.app.router.add_route("GET", path, AIOHTTPMethodHandler)

    async def start(self) -> None:
        """
        Starts the log viewer server.
        """
        if self._running:
            raise RuntimeError("Log viewer server is already running.")
        if not self._hooked:
            self.init_hook()
        logger.info("Starting log viewer server.")
        self.runner = web.AppRunner(self.app, handle_signals=True)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.config.host, self.config.port)
        await self.site.start()
        favicon_path = static_path / "favicon.webp"
        if not favicon_path.exists():
            asset = self.bot.user.display_avatar.replace(size=32, format="webp")
            try:
                await asset.save(favicon_path)
            except discord.NotFound as exc:
                logger.error("Unable to set 'favicon.webp' due to download failure.")
                logger.error(f"{type(exc).__name__}: {str(exc)}")
        self._running = True

    async def stop(self) -> None:
        """
        Stops the log viewer server.
        """
        logger.warning(" - Shutting down web server. - ")
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()
        self._running = False

    def is_running(self) -> bool:
        """Returns `True` if the server is currently running."""
        return self._running

    def info(self) -> str:
        """Returns modules used to run the web server."""
        main_deps = (
            f"Web application: aiohttp v{aiohttp.__version__}\n"
            f"Template renderer: jinja2 v{jinja2.__version__}\n"
        )

        return main_deps

    async def process_logs(self, request: Request, *, path: str, key: str, **kwargs) -> Response:
        """
        Matches the request path with regex before rendering the logs template to user.
        """
        path_re = re.compile(rf"^{self.config.log_prefix}/(?:(?P<raw>raw)/)?(?P<key>([a-zA-Z]|[0-9])+)")
        match = path_re.match(path)
        if match is None:
            return await self.raise_error("not_found", message=f"Invalid path, '{path}'.")
        data = match.groupdict()
        raw = data["raw"]
        if not raw:
            return await self.render_logs(request, key, **kwargs)
        else:
            return await self.render_raw_logs(request, key, **kwargs)

    @authentication
    async def render_logs(
        self,
        request: Request,
        key: str,
        **kwargs,
    ) -> Response:
        """Returns the html rendered log entry"""
        logs = self.bot.api.logs
        document: RawPayload = await logs.find_one({"key": key})
        if not document:
            return await self.raise_error("not_found", message=f"Log entry '{key}' not found.")
        log_entry = LogEntry(document)
        return await self.render_template("logbase", request, log_entry=log_entry, **kwargs)

    @authentication
    async def render_raw_logs(self, request, key, **kwargs) -> Any:
        """
        Returns the plain text rendered log entry.
        """
        logs = self.bot.api.logs
        document: RawPayload = await logs.find_one({"key": key})
        if not document:
            return await self.raise_error("not_found", message=f"Log entry '{key}' not found.")

        log_entry = LogEntry(document)
        return Response(
            status=200,
            text=log_entry.plain_text(),
            content_type="text/plain",
            charset="utf-8",
        )
    
    @authentication
    async def render_loglist(self, request, **kwargs) -> Any:
        """
        Returns the html rendered log list
        """
        logs = self.bot.api.logs

        logs_per_page = int(self.config.pagination)
        
        try:
            page = int(request.query.get("page", 1))
        except ValueError:
            page = 1

        def parse_date(date):
            date = dateutil.parser.parse(date).astimezone(timezone.utc)
            timestamp = duration(date, datetime.now(timezone.utc))
            return timestamp

        async def find_logs():
            filter_ = {"bot_id": str(self.bot.user.id)}

            count_all = await logs.count_documents(filter=filter_)

            status_open = request.query.get("open")

            if status_open == "false":
                filter_["open"] = False
            elif status_open == "true":
                filter_["open"] = True
            else:
                status_open = None

            if request.query.get("search"):
                search = request.query.get("search")
                filter_["$text"] = {"$search": search}

            projection_ = {
                "key": 1,
                "open": 1,
                "created_at": 1,
                "closed_at": 1,
                "recipient": 1,
                "creator": 1,
                "title": 1,
                "last_message": {"$arrayElemAt": ["$messages", -1]},
                "message_count": {"$size": "$messages"},
                "nsfw": 1,
            }

            cursor = logs.find(
                filter=filter_,
                projection=projection_,
                skip=(page - 1) * logs_per_page,
            ).sort("created_at", -1)

            count = await logs.count_documents(filter=filter_)

            max_page = count // logs_per_page
            if (count % logs_per_page) > 0:
                max_page += 1

            items = await cursor.to_list(length=logs_per_page)

            # iterate over list to change timestamps to readable format
            # also reduce size of author avatar
            for index, item in enumerate(items):
                recipient_avatar_url = items[index]["recipient"][
                    "avatar_url"
                ].split("?")[0]
                items[index]["recipient"]["avatar_url"] = recipient_avatar_url

                creator_avatar_url = items[index]["creator"]["avatar_url"].split(
                    "?"
                )[0]
                items[index]["creator"]["avatar_url"] = creator_avatar_url

                creation_date = item.get("created_at")
                items[index].update(created_at=parse_date(creation_date))
                close_date = item.get("closed_at")

                if close_date is not None:
                    items[index].update(closed_at=parse_date(close_date))

                try:
                    last_message = items[index].get("last_message")
                    last_message_duration = parse_date(
                        last_message.get("timestamp")
                    )
                    items[index]["last_message_time"] = last_message_duration
                except Exception:
                    pass

            return items, max_page, status_open, count_all
        
        prefix = self.config.log_prefix

        document, max_page, status_open, count_all = await find_logs()

        log_list = LogList(document, prefix, page, max_page, status_open, count_all)

        return await self.render_template("loglist", request, data=log_list, **kwargs)

    @staticmethod
    async def raise_error(error_type: str, *, message: Optional[str] = None, **kwargs) -> Any:
        exc_mapping = {
            "not_found": web.HTTPNotFound,
            "error": web.HTTPInternalServerError,
        }
        try:
            ret = exc_mapping[error_type]
        except KeyError:
            ret = web.HTTPInternalServerError
        if "status_code" in kwargs:
            status = kwargs.pop("status_code")
            kwargs["status"] = status

        if message is None:
            message = "No error message."
        raise ret(reason=message, **kwargs)

    async def render_template(
        self,
        name: str,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            session = await get_session(request)
        kwargs["app"] = request.app
        kwargs["config"] = self.config
        kwargs["using_oauth"] = True
        kwargs["session"] = session
        kwargs["user"] = session.get("user")
        kwargs["logged_in"] = kwargs["user"] is not None

        template = jinja_env.get_template(name + ".html")
        template = await template.render_async(*args, **kwargs)
        response = Response(
            status=200,
            content_type="text/html",
            charset="utf-8",
        )
        response.text = template
        return response
