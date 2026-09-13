import logging

import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger("esmo")

ACCESS_TOKEN_CACHE_KEY = "esmo_oauth_access_token"


class EsmoAuthError(Exception):
    """Raised when an access token cannot be obtained from the ESMO API."""


def _client_id():
    """Passport expects a numeric client_id, but keep strings working too."""
    value = settings.ESMO_CLIENT_ID
    return int(value) if str(value).isdigit() else value


def _credentials_configured() -> bool:
    required = [settings.ESMO_CLIENT_ID, settings.ESMO_CLIENT_SECRET]
    if settings.ESMO_GRANT_TYPE == "password":
        required += [settings.ESMO_USERNAME, settings.ESMO_PASSWORD]
    return all(required)


async def _request_token(payload: dict) -> dict:
    """POST to the Passport token endpoint. The payload is never logged."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "X-TZ-Offset": str(settings.ESMO_TZ_OFFSET),
    }
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            settings.ESMO_OAUTH_TOKEN_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

    if response.status_code >= 400:
        raise EsmoAuthError(
            f"{response.status_code} from {settings.ESMO_OAUTH_TOKEN_URL} "
            f"for grant_type={payload.get('grant_type')}"
        )

    data = response.json()
    if not data.get("access_token"):
        raise EsmoAuthError("Token endpoint returned no access_token")
    return data


def _store(data: dict) -> str:
    expires_in = int(data.get("expires_in", 0))
    ttl = max(expires_in - settings.ESMO_TOKEN_LEEWAY, 60)
    cache.set(ACCESS_TOKEN_CACHE_KEY, data["access_token"], ttl)
    logger.info(
        "Obtained a new ESMO access token (expires_in=%s, cached for %s seconds)",
        expires_in,
        ttl,
    )
    return data["access_token"]


async def _login() -> str:
    payload = {
        "grant_type": settings.ESMO_GRANT_TYPE,
        "client_id": _client_id(),
        "client_secret": settings.ESMO_CLIENT_SECRET,
    }
    if settings.ESMO_GRANT_TYPE == "password":
        payload["username"] = settings.ESMO_USERNAME
        payload["password"] = settings.ESMO_PASSWORD
    return _store(await _request_token(payload))


async def get_access_token(force_new: bool = False) -> str:
    """Return a cached access token, obtaining a new one when needed.

    Falls back to the static TOKEN env var when no OAuth credentials are set,
    so deployments that still carry a hand-issued token keep working.
    """
    if not _credentials_configured():
        if settings.TOKEN:
            return settings.TOKEN
        raise EsmoAuthError(
            "No ESMO OAuth credentials configured (ESMO_CLIENT_ID, ESMO_CLIENT_SECRET"
            ", ESMO_USERNAME, ESMO_PASSWORD) and no static TOKEN to fall back on"
        )

    if force_new:
        cache.delete(ACCESS_TOKEN_CACHE_KEY)
    else:
        token = cache.get(ACCESS_TOKEN_CACHE_KEY)
        if token:
            return token

    return await _login()
