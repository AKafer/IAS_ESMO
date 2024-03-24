import httpx
import logging

logger = logging.getLogger("esmo")


class BaseApiClient:

    async def make_request(self, method, url, headers, data):
        async with httpx.AsyncClient(verify=False) as client:
            logger.debug(
                "Requesting [%s] %s", method.upper(), url, extra={"payload": data or {}}
            )
            try:
                response = await client.request(method, url, json=data, headers=headers)
            except httpx.HTTPError as e:
                print('AAAAAAAAAAAAAAAAAAAAAAAAAAA')
                print(e)
                logger.error(
                    "Exception occurred while trying to request [%s] %s",
                    method,
                    url,
                    exc_info=e,
                    extra={"payload": data or {}},
                )
                raise e
            except Exception as e:
                print('BBBBBBBBBBBBBBBBBBBB')
                print(e)
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
