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


async def main():
    proxy = 'socks5://amcTW8cm:PM3EESuL@154.194.103.215:64633'

    res = await async_get('http://eth0.me/', proxy=proxy)
    print(res)


if __name__ == '__main__':
    asyncio.run(main())
