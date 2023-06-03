import os
import warnings
from urllib.parse import urlencode

import aiohttp
from aiohttp_session import get_session

from core.models import getLogger

logger = getLogger(__name__)

OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI = os.getenv("OAUTH2_REDIRECT_URI")

API_BASE = "https://discordapp.com/api/"
AUTHORIZATION_BASE_URL = f"{API_BASE}/oauth2/authorize"
TOKEN_URL = f"{API_BASE}/oauth2/token"
ROLE_URL = f"{API_BASE}/guilds/{{guild_id}}/members/{{user_id}}"


def authentication(func):
    async def wrapper(self, request, key=None, **kwargs):
        if not self.config.using_oauth:
            result = await func(self, request, key=key or None, **kwargs)
            return result
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
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
            kwargs["using_oauth"] = True
            kwargs["session"] = session
            kwargs["user"] = user
            kwargs["logged_in"] = kwargs["user"] is not None
            kwargs.update(globals())
            result = await func(self, request, key=key or None, **kwargs)
            return result
        
        result = await self.render_template(
            "unauthorized", request, message="You are not authorized to view this thread."
        )
        return result
    return wrapper

async def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f"{API_BASE}/users/@me", headers=headers)
        user = await resp.json()
        return user
        
async def get_user_roles(user_id):
    _guild_id = os.getenv("GUILD_ID", None)
    _bot_token = os.getenv("TOKEN", None)
    url = ROLE_URL.format(guild_id=_guild_id, user_id=user_id)
    headers = {"Authorization": f"Bot {_bot_token}"}
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=headers)
        user = await resp.json()
        user_roles = user.get("roles", [])
        return user_roles

async def fetch_token(code):
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": OAUTH2_REDIRECT_URI,
        "client_id": OAUTH2_CLIENT_ID,
        "client_secret": OAUTH2_CLIENT_SECRET,
        "scope": "identify",
    }

    async with aiohttp.ClientSession() as session:
        resp = await session.post(TOKEN_URL, data=data)
        json = await resp.json()
        return json
    
async def login(request):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        session = await get_session(request)
    session.invalidate()
    raise aiohttp.web.HTTPFound("/")