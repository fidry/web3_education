from libs.eth_async.utils.web_requests import aiohttp_params
from libs.py_okx_async.Base import Base
from libs.py_okx_async.models import Methods, FundingToken
from libs.py_okx_async.subaccount.models import SubaccountInfo
from libs.py_okx_async.utils import secs_to_millisecs


class Subaccount(Base):
    """
    The class contains functions from the 'subaccount' section.

    Attributes:
        section (str): a section name.

    """
    section: str = 'subaccount'

    async def list(
            self, enable: bool | None = None, subAcct: str | None = None, after: int | None = None,
            before: int | None = None, limit: int = 100
    ) -> dict[str, SubaccountInfo]:
        """
        Get a dictionary with sub-account names and information about them.

        Args:
            enable (Optional[bool]): sub-account status. true: Normal false: Frozen. (absolutely all)
            subAcct (Optional[str]): sub-account name. (absolutely all)
            after (Optional[int]): if you query the data prior to the requested creation time ID, the value
                will be a Unix timestamp in millisecond format. (None)
            before (Optional[int]): if you query the data after the requested creation time ID, the value
                will be a Unix timestamp in millisecond format. (None)
            limit (int): number of results per request, the maximum is 100. (100)

        Returns:
            dict[str, SubaccountInfo]: the dictionary with sub-account names and information about them.

        """
        method = 'list'
        body = {
            'enable': enable,
            'subAcct': subAcct,
            'limit': limit
        }

        if after:
            body['after'] = await secs_to_millisecs(secs=after)

        if before:
            body['before'] = await secs_to_millisecs(secs=before)

        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/users/{self.section}/{method}', body=aiohttp_params(body)
        )
        subaccounts = {}
        for token in response.get('data'):
            subaccounts[token.get('subAcct')] = SubaccountInfo(data=token)

        return subaccounts

    async def asset_balances(self, subAcct: str, token_symbol: str | None = None) -> dict[str, FundingToken]:
        """
        Get a dictionary with tokens and their balances in the funding account of a sub-account.

        Args:
            subAcct (str): sub-account name.
            token_symbol (Optional[str]): single or multiple token symbol (no more than 20) separated
                with comma, e.g. BTC or BTC,ETH. (absolutely all)

        Returns:
            dict[str, FundingToken]: the dictionary with tokens and their balances in the funding account
                of a sub-account.

        """
        method = 'balances'
        body = {
            'subAcct': subAcct,
            'ccy': token_symbol
        }
        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/asset/{self.section}/{method}', body=aiohttp_params(body)
        )
        tokens = {}
        for token in response.get('data'):
            tokens[token.get('ccy')] = FundingToken(data=token)

        return tokens
