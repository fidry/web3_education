import random
from typing import Optional, Union
from decimal import Decimal

import aiohttp
from aiohttp_proxy import ProxyConnector

from loguru import logger


def get_explorer_hash_link(tx_hash: str):
    try:
        return f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=mainnet"
    except Exception as e:
        logger.error(f"Ge"
                     f"t explorer hash link error: {str(e)}")


def randfloat(from_: Union[int, float, str], to_: Union[int, float, str],
              step: Optional[Union[int, float, str]] = None) -> float:
    from_ = Decimal(str(from_))
    to_ = Decimal(str(to_))
    if not step:
        step = 1 / 10 ** (min(from_.as_tuple().exponent, to_.as_tuple().exponent) * -1)

    step = Decimal(str(step))
    rand_int = Decimal(str(random.randint(0, int((to_ - from_) / step))))
    return float(rand_int * step + from_)


def prepare_address_for_aptoscan_api(address: str):
    if address.startswith('0x'):
        address = address[2:]
    result_address = '0x'

    beginning_word = True
    for ch in address:
        if beginning_word:
            if ch != '0':
                beginning_word = False
            else:
                continue
        result_address += ch
    return result_address


async def async_get(
        url: str,
        proxy: str | None = None,
        headers: dict | None = None,
        **kwargs
) -> tuple[int, dict] | None:

    connector = ProxyConnector.from_url(
        url=proxy
    ) if proxy else None

    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        async with session.get(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return status_code, response
    return None


async def async_post(
        url: str,
        proxy: str | None = None,
        headers: Optional[dict] = None,
        **kwargs
) -> tuple[int, dict] | None:

    connector = ProxyConnector.from_url(
        url=proxy
    ) if proxy else None

    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        async with session.post(url=url, **kwargs) as response:
            status_code = response.status
            response = await response.json(encoding='utf-8')
            if status_code <= 201:
                return status_code, response

    return None
