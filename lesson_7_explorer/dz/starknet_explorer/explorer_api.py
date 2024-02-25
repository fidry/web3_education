import random

from fake_useragent import UserAgent

from starknet_explorer.utils import async_get, aiohttp_params


class Module:
    """
    Class with functions related to some API module.

    Attributes:
        url (str): an API entrypoint URL.
        module (str): a module name.

    """
    url: str
    module: str

    def __init__(self, url: str) -> None:
        """
        Initialize the class.

        Args:
            url (str): an API entrypoint URL.

        """
        self.url = url


class Account(Module):
    module: str = 'contracts'

    async def txlist(
            self,
            address: str,
            page: int = 1,
    ) -> dict:
        """
        Query address transaction list information

        https://viewblock.io/starknet
        """

        action = 'txs'

        headers = {
            'authority': 'api.viewblock.io',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://viewblock.io',
            'referer': 'https://viewblock.io/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent().random,
        }

        params = {
            'page': str(page),
            'network': 'mainnet',
        }

        return await async_get(
            url=f'{self.url}/{self.module}/{address}/{action}',
            params=aiohttp_params(params),
            headers=headers
        )

    async def txlist_all(self, address: str) -> list[dict]:
        page = 1
        txs_lst = []

        data = await self.txlist(address=address, page=page)
        pages, txs = data.get('pages', 0), data.get('docs', [])

        txs_lst += txs
        if pages == 0:
            return []
        while page != pages:
            page += 1

            data = await self.txlist(address=address, page=page)
            pages, txs = data.get('pages', 0), data.get('docs', [])

            txs_lst += txs
        return txs_lst


class APIFunctions:
    """
    Class with functions related to Blockscan API.

    Attributes:
        url (str): an API entrypoint URL.
        account (Account): functions related to 'account' API module.

    """

    def __init__(self, url: str) -> None:
        """
        Initialize the class.

        Args:
            url (str): an API entrypoint URL.

        """
        self.url = url
        self.account = Account(self.url)
