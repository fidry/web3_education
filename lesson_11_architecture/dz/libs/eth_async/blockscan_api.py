from fake_useragent import UserAgent

from libs.eth_async.exceptions import APIException
from libs.eth_async.utils.web_requests import async_get, aiohttp_params


class Tag:
    """
    An instance with tag values.
    """
    Earliest: str = 'earliest'
    Pending: str = 'pending'
    Latest: str = 'latest'


class Sort:
    """
    An instance with sort values.
    """
    Asc: str = 'asc'
    Desc: str = 'desc'


class Module:
    """
    Class with functions related to some API module.

    Attributes:
        key (str): an API key.
        url (str): an API entrypoint URL.
        headers (Dict[str, Any]): a headers for requests.
        module (str): a module name.

    """
    key: str
    url: str
    headers: dict[str, ...]
    module: str

    def __init__(self, key: str, url: str, headers: dict[str, ...]) -> None:
        """
        Initialize the class.

        Args:
            key (str): an API key.
            url (str): an API entrypoint URL.
            headers (Dict[str, Any]): a headers for requests.

        """
        self.key = key
        self.url = url
        self.headers = headers


class Account(Module):
    """
    Class with functions related to 'account' API module.
    """
    module: str = 'account'

    async def balance(self, address: str, tag: str = Tag.Latest) -> dict[str, ...]:
        """
        Return the Ether balance of a given address.

        https://docs.etherscan.io/api-endpoints/accounts#get-ether-balance-for-a-single-address

        Args:
            address (str): the address to check for balance
            tag (Union[str, Tag]): the pre-defined block parameter, either "earliest", "pending" or "latest". ("latest")

        Returns:
            Dict[str, Any]: the dictionary with the Ether balance of the address in wei.

        """
        action = 'balance'
        if tag not in (Tag.Earliest, Tag.Earliest, Tag.Latest):
            raise APIException('"tag" parameter have to be either "earliest", "pending" or "latest"')

        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'tag': tag,
            'apikey': self.key,
        }
        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)

    async def balancemulti(self, address: list[str], tag: str = Tag.Latest):
        action = 'balancemulti'

        if tag not in (Tag.Earliest, Tag.Earliest, Tag.Latest):
            raise APIException('"tag" parameter have to be either "earliest", "pending" or "latest"')

        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'tag': tag,
            'apikey': self.key,
        }
        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)

    async def txlist(
            self, address: str, startblock: int | None = None, endblock: int | None = None,
            page: int | None = None, offset: int | None = None, sort: str | Sort = Sort.Asc
    ) -> dict[str, ...]:
        """
        Return the list of transactions performed by an address, with optional pagination.

        https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address

        Args:
            address (str): the address to get the transaction list.
            startblock (Optional[int]): the block number to start searching for transactions.
            endblock (Optional[int]): the block number to stop searching for transactions.
            page (Optional[int]): the page number, if pagination is enabled.
            offset (Optional[int]): the number of transactions displayed per page.
            sort (Union[str, Sort]): the sorting preference, use "asc" to sort by ascending and "desc" to sort
                by descending. ("asc")

        Returns:
            Dict[str, Any]: the dictionary with the list of transactions performed by the address.

        """
        action = 'txlist'
        if sort not in ('asc', 'desc'):
            raise APIException('"sort" parameter have to be either "asc" or "desc"')

        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'startblock': startblock,
            'endblock': endblock,
            'page': page,
            'offset': offset,
            'sort': sort,
            'apikey': self.key,
        }

        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)

    async def txlistinternal(
            self,
            address: str,
            startblock: int | None = None,
            endblock: int | None = None,
            page: int = 1,
            offset: int = 0,
            sort: str = Sort.Asc
    ):
        action = 'txlistinternal'

        if sort not in ('asc', 'desc'):
            raise APIException('"sort" parameter have to be either "asc" or "desc"')

        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'startblock': startblock,
            'endblock': endblock,
            'page': page,
            'offset': offset,
            'sort': sort,
            'apikey': self.key,
        }

        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)

    async def tokentx(
            self,
            contractaddress: str,
            address: str,
            page: int = 1,
            offset: int = 0,
            startblock: int | None = None,
            endblock: int | None = None,
            sort: str = Sort.Asc
    ):
        action = 'tokentx'

        if sort not in ('asc', 'desc'):
            raise APIException('"sort" parameter have to be either "asc" or "desc"')

        params = {
            'module': self.module,
            'action': action,
            'contractaddress': contractaddress,
            'address': address,
            'page': page,
            'offset': offset,
            'startblock': startblock,
            'endblock': endblock,
            'sort': sort,
            'apikey': self.key,
        }

        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)


class Contract(Module):
    """
    Class with functions related to 'contract' API module.
    """
    module: str = 'contract'

    async def getabi(self, address: str) -> dict[str, ...]:
        """
        Return the Contract Application Binary Interface (ABI) of a verified smart contract.

        https://docs.etherscan.io/api-endpoints/contracts#get-contract-abi-for-verified-contract-source-codes

        Args:
            address (str): the contract address that has a verified source code.

        Returns:
            Dict[str, Any]: the dictionary with the contract ABI.

        """
        action = 'getabi'
        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'apikey': self.key,
        }
        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)

    async def getsourcecode(self, address: str):
        action = 'getsourcecode'

        params = {
            'module': self.module,
            'action': action,
            'address': address,
            'apikey': self.key,
        }
        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)


class Transaction(Module):
    module: str = 'transaction'

    async def getstatus(self, txhash: str):
        action = 'getstatus'

        params = {
            'module': self.module,
            'action': action,
            'txhash': txhash,
            'apikey': self.key,
        }
        return await async_get(self.url, params=aiohttp_params(params), headers=self.headers)


class APIFunctions:
    """
    Class with functions related to Blockscan API.

    Attributes:
        key (str): an API key.
        url (str): an API entrypoint URL.
        headers (Dict[str, Any]): a headers for requests.
        account (Account): functions related to 'account' API module.
        contract (Contract): functions related to 'contract' API module.
        transaction (Transaction): functions related to 'transaction' API module.
        block (Block): functions related to 'block' API module.
        logs (Logs): functions related to 'logs' API module.
        token (Token): functions related to 'token' API module.
        gastracker (Gastracker): functions related to 'gastracker' API module.
        stats (Stats): functions related to 'stats' API module.

    """

    def __init__(self, key: str, url: str) -> None:
        """
        Initialize the class.

        Args:
            key (str): an API key.
            url (str): an API entrypoint URL.

        """
        self.key = key
        self.url = url
        self.headers = {'content-type': 'application/json', 'user-agent': UserAgent().chrome}
        self.account = Account(self.key, self.url, self.headers)
        self.contract = Contract(self.key, self.url, self.headers)
        self.transaction = Transaction(self.key, self.url, self.headers)
        # self.block = Block(self.key, self.url, self.headers)
        # self.logs = Logs(self.key, self.url, self.headers)
        # self.token = Token(self.key, self.url, self.headers)
        # self.gastracker = Gastracker(self.key, self.url, self.headers)
        # self.stats = Stats(self.key, self.url, self.headers)
