from functools import wraps

import aiohttp
from aiohttp_session import get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import os

from urllib.parse import urlencode

OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI = os.getenv("OAUTH2_REDIRECT_URI")

API_BASE = "https://discordapp.com/api/"
AUTHORIZATION_BASE_URL = f"{API_BASE}/oauth2/authorize"
TOKEN_URL = f"{API_BASE}/oauth2/token"
ROLE_URL = f"{API_BASE}/guilds/{{guild_id}}/members/{{user_id}}"

from core.models import getLogger

logger = getLogger(__name__)

client_session = aiohttp.ClientSession()


def authentication(func):
    async def wrapper(self, request, **kwargs):
        if not self.config.using_oauth:
            result = await func(self, request, **kwargs)
            return result

        session = await get_session(request)
        if not session.get("user"):
            session["last_visit"] = str(request.url)
            raise aiohttp.web.HTTPFound("/login")

        user = session.get("user")

        whitelist = self.bot.config.get("oauth_whitelist", [])

        roles = await get_user_roles(user["id"])

        if (
            int(user["id"]) in whitelist or 
            "everyone" in whitelist or
            any(int(r) in whitelist for r in roles)
        ):
            result = await func(self, request, **kwargs)
            return result
        
        result = await self.render_template("unauthorized", request)

        return result
    return wrapper


def authrequired():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, request):
            if self.config.using_oauth:
                session = await get_session(request)
                if not session.get("user"):
                    session["last_visit"] = str(request.url)
                    raise aiohttp.web.HTTPFound("/login")

                user = session.get("user")
                logger.info(user)

                whitelist = self.bot.config.get("oauth_whitelist", [])

                roles = await get_user_roles(user["id"])

                if (
                    int(user["id"]) not in whitelist and 
                    "everyone" not in whitelist and
                    any(int(r) not in whitelist for r in roles)
                ):
                    logger.warn("Unauthorized access detected")
                    return await self.render_template("unauthorized")

        return wrapper

    return decorator

async def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    async with client_session.get(
        f"{API_BASE}/users/@me", headers=headers
    ) as resp:
        _r = await resp.json()
        logger.info(f"UINFO: {_r}")
        return await resp.json()
        
async def get_user_roles(user_id):
    _guild_id = os.getenv("GUILD_ID", None)
    _bot_token = os.getenv("BOT_TOKEN", None)
    url = ROLE_URL.format(guild_id=_guild_id, user_id=user_id)
    headers = {"Authorization": f"Bot {_bot_token}"}
    async with client_session.get(url, headers=headers) as resp:
        user = await resp.json()
    return user.get("roles", [])

async def fetch_token(code):
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": OAUTH2_REDIRECT_URI,
        "client_id": OAUTH2_CLIENT_ID,
        "client_secret": OAUTH2_CLIENT_SECRET,
        "scope": "identify",
    }

    async with client_session.post(TOKEN_URL, data=data) as resp:
        json = await resp.json()
        return json
    
async def login(request):
    session = await get_session(request)
    if not session.get("last_visit"):
        session["last_visit"] = "/"

    data = {
        "scope": "identify",
        "client_id": OAUTH2_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": OAUTH2_REDIRECT_URI,
    }

    raise aiohttp.web.HTTPFound(f"{AUTHORIZATION_BASE_URL}?{urlencode(data)}")

async def oauth_callback(request):
    session = await get_session(request)

    code = request.query.get("code")
    token = await fetch_token(code)
    access_token = token.get("access_token")
    if access_token is not None:
        session["access_token"] = access_token
        session["user"] = await get_user_info(access_token)
        url = "/"
        if "last_visit" in session:
            url = session["last_visit"]
        raise aiohttp.web.HTTPFound(url)
    raise aiohttp.web.HTTPFound("/login")

async def logout(request):
    session = await get_session(request)
    session.invalidate()
    raise aiohttp.web.HTTPFound("/")