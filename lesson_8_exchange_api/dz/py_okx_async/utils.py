from typing import Union, Dict, Any, Optional

import aiohttp
from aiohttp_socks import ProxyConnector

from py_okx_async import exceptions


def aiohttp_params(params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Union[str, int, float]]]:
    """
    Convert requests params to aiohttp params.

    :param Optional[Dict[str, Any]] params: requests params
    :return Optional[Dict[str, Union[str, int, float]]]: aiohttp params
    """
    new_params = params.copy()
    if not params:
        return

    for key, value in params.items():
        if value is None:
            del new_params[key]

        if isinstance(value, bool):
            new_params[key] = str(value).lower()

        elif isinstance(value, bytes):
            new_params[key] = value.decode('utf-8')

    return new_params


async def async_get(
        url: str, headers: Optional[dict] = None, connector: Optional[ProxyConnector] = None, **kwargs
) -> Optional[dict]:
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
    # todo: надо раскомментировать, чтобы работать с прокси
    # async with aiohttp.ClientSession(headers=headers, connector=connector, connector_owner=False) as session:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return response

            raise exceptions.APIException(response=response, status_code=status_code)


async def async_post(
        url: str, headers: Optional[dict] = None, connector: Optional[ProxyConnector] = None, **kwargs
) -> Optional[dict]:
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
    # todo: надо раскомментировать, чтобы работать с прокси
    # async with aiohttp.ClientSession(headers=headers, connector=connector, connector_owner=False) as session:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return response

            raise exceptions.APIException(response=response, status_code=status_code)


async def secs_to_millisecs(secs: Union[int, float, str]) -> int:
    secs = int(secs)
    return secs * 1000 if len(str(secs)) == 10 else secs
