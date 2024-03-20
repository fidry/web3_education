import aiohttp
from aiohttp_socks import ProxyConnector

from libs.py_okx_async import exceptions


async def async_get(
        url: str, headers: dict | None = None, connector: ProxyConnector | None = None, **kwargs
) -> dict | None:
    """
    Make asynchronous GET request.

    Args:
        url (str): a URL.
        headers (Optional[dict]): headers. (None)
        connector (Optional[ProxyConnector]): a connector. (None)
        kwargs: arguments for a GET request, e.g. 'params', 'data' or 'json'.

    Returns:
        Optional[dict]: a JSON response to request.

    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return response

            raise exceptions.APIException(response=response, status_code=status_code)


async def async_post(
        url: str, headers: dict | None = None, connector: ProxyConnector | None = None, **kwargs
) -> dict | None:
    """
    Make asynchronous POST request.

    Args:
        url (str): a URL.
        headers (Optional[dict]): headers. (None)
        connector (Optional[ProxyConnector]): a connector. (None)
        kwargs: arguments for a POST request, e.g. 'params', 'data' or 'json'.

    Returns:
        Optional[dict]: a JSON response to request.

    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return response

            raise exceptions.APIException(response=response, status_code=status_code)


async def secs_to_millisecs(secs: int | float | str) -> int:
    secs = int(secs)
    return secs * 1000 if len(str(secs)) == 10 else secs
