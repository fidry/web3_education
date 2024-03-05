import aiohttp
import asyncio
from aiohttp_proxy import ProxyConnector

# https://pypi.org/project/aiohttp-proxy/


async def async_get(
        url: str,
        proxy: str | None = None,
        headers: dict | None = None,
        **kwargs
) -> dict | str | None:

    connector = ProxyConnector.from_url(
        url=proxy
    ) if proxy else None

    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        async with session.get(url=url, **kwargs) as response:
            status_code = response.status
            # response = await response.json()
            response = await response.text()
            if status_code <= 201:
                return response
    return None


async def change_mobile_ip(change_ip_url: str) -> bool:
    try:
        response = await async_get(url=change_ip_url)
        print(response)
        return True
    except Exception as e:
        return False


async def main():
    proxy = 'http://228e532527:2e25236787@92.255.251.69:40962'

    change_ip_url = ('https://proxys.io/ru/api/v2/change-mobile-proxy-ip'
                     '?key=10be37368e08eee1b2f2ccca5d012762'
                     '&order=21569'
                     '&proxy=1'
                     )

    res = await async_get('http://eth0.me/', proxy=proxy)
    print(res)

    # await change_mobile_ip(change_ip_url=change_ip_url)


if __name__ == '__main__':
    asyncio.run(main())
