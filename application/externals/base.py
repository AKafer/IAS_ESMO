import asyncio
from datetime import timedelta

import httpx
import logging

from django.conf import settings
from failsafe import Failsafe, RetryPolicy, Delay, FailsafeError

logger = logging.getLogger("esmo")


class BaseApiClient:
    allowed_retries: int = settings.ALLOWED_RETRIES
    backoff_seconds: float = settings.BACKOFF_SECONDS
    abortable_exceptions: list[Exception] = []
    retriable_exceptions: list[Exception] = [
        TimeoutError,
        httpx.ReadTimeout,
        httpx.ConnectTimeout,
        httpx.RequestError,
        asyncio.exceptions.TimeoutError,
    ]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.failsafe = self._init_failsafe()

    def _init_failsafe(self) -> Failsafe:
        retry_policy = RetryPolicy(
            allowed_retries=self.allowed_retries,
            backoff=Delay(timedelta(seconds=self.backoff_seconds)),
            abortable_exceptions=self.abortable_exceptions,
            retriable_exceptions=self.retriable_exceptions
        )
        return Failsafe(retry_policy=retry_policy)

    async def request(self, method, url, headers=None, data=None):
        print(f"URL {url}")
        async with httpx.AsyncClient(verify=False) as client:
            return await client.request(method, url, headers=headers, json=data)

    async def make_request(self, method, url, headers, data):
        logger.debug(
            "Requesting [%s] %s", method.upper(), url, extra={"payload": data or {}}
        )
        try:
            response = await self.failsafe.run(
                lambda: self.request(method, url, data=data, headers=headers)
            )
        except FailsafeError as e:
            logger.error(
                "Failsafe error occurred while trying to request [%s] %s",
                method,
                url,
                exc_info=e,
                extra={"payload": data or {}},
            )
            raise e
        logger.debug(
            "Received [%s] response from %s",
            response.status_code,
            url,
            extra={
                "payload": f"{response.text[:1000]}..."
                if response.text else "{}",
            }
        )
        return response

    async def get(self, url, headers=None, data=None):
        response = await self.make_request("GET", url, data=data, headers=headers)
        return await self._deserialize_response(response)

    async def post(self, url, headers=None, data=None):
        response = await self.make_request("POST", url, data=data, headers=headers)
        return await self._deserialize_response(response)

    async def put(self, url, headers=None, data=None):
        response = await self.make_request("PUT", url, data=data, headers=headers)
        return await self._deserialize_response(response)

    async def patch(self, url, headers=None, data=None):
        response = await self.make_request("PATCH", url, data=data, headers=headers)
        return await self._deserialize_response(response)

    async def delete(self, url, headers=None, data=None):
        response = await self.make_request("DELETE", url, data=data, headers=headers)
        return await self._deserialize_response(response)

    @staticmethod
    async def _deserialize_response(response):
        if response.status_code >= 400:
            if isinstance(response.content, bytes):
                reason = response.content.decode("utf")
            else:
                reason = (response.content,)

            side = "Client" if response.status_code < 500 else "Server"
            error_message = (
                f"{response.status_code} {side} Error: {reason} for url: {response.url}"
            )
            logger.error(error_message)
            raise httpx.RequestError(error_message)

        if not response.text:
            return None

        try:
            data = response.json()
        except ValueError as err:
            err_msg = f"Failed to deserialize response content. Error: {err}"
            logger.error(err_msg)
            raise httpx.DecodingError(err_msg)

        return data
