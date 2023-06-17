from __future__ import annotations

import os
from typing import TYPE_CHECKING, Callable

from aiohttp import web
from aiohttp.web import Response

from core.models import getLogger

from .auth import login, logout, oauth_callback

if TYPE_CHECKING:
    from aiohttp.web import Request


logger = getLogger(__name__)


@web.middleware
async def aiohttp_error_handler(
    request: Request,
    handler: Callable[[Request], Response],
) -> Response:
    status_map = {
        404: "not_found",
        500: "error",
    }
    server = request.app["server"]
    try:
        return await handler(request)
    except web.HTTPException as exc:
        status = exc.status
        if status < 400:
            # This includes redirect
            raise
        if status in status_map:
            return await server.render_template(status_map[status], request)

        logger.error(f"Status code: {status}")
        logger.error("Exception: %s", str(exc))
        logger.error(
            "Unexpected exception: %s",
            type(exc).__name__,
            exc_info=True,
        )
        if status >= 500:
            return await server.render_template("error", request)
        raise


class AIOHTTPMethodHandler(web.View):
    """
    Represents HTTP handler. Every incoming HTTP requests will be handled from this class.
    """

    async def head(self) -> Response:
        return Response(
            status=200,
            text="OK!",
            content_type="text/plain",
            charset="utf-8",
        )

    async def get(self) -> Response:
        """
        Every `GET` requests is handled from here.
        """
        params = self.request.match_info
        path = self.request.path
        key = params.get("key")
        server = self.request.app["server"]

        log_prefix = os.getenv("LOG_URL_PREFIX", "/logs")

        if log_prefix == "/" and path == "/":
            return await server.render_loglist(self.request)

        if path == log_prefix:
            return await server.render_loglist(self.request)
        
        if path == "/login":
            return await login(self.request)
        
        if path == "/callback":
            return await oauth_callback(self.request)
        
        if path == "/logout":
            return await logout(self.request)
        
        if path == "/":
            return await server.render_template("index", self.request)
        
        if key:
            return await server.process_logs(self.request, path=self.request.path, key=key)

        raise web.HTTPNotFound(reason=f"Invalid path, '{self.request.path}'.")
