from typing import Optional, Dict, Union

from libs.eth_async.utils.web_requests import aiohttp_params

from libs.py_okx_async.Base import Base
from libs.py_okx_async.asset.models import (
    Currency, TransactionType, TransactionTypes, WithdrawalStatus, Withdrawal, WithdrawalToken, TransferType,
    TransferTypes, Transfer, DepositStatus, Deposit
)
from libs.py_okx_async.models import Methods, FundingToken, AccountType, AccountTypes
from libs.py_okx_async.utils import secs_to_millisecs


class Asset(Base):
    """
    The class contains functions from the 'asset' section.

    Attributes:
        section (str): a section name.

    """
    section: str = 'asset'

    async def currencies(self, token_symbol: Optional[str] = None) -> Dict[str, Dict[str, Currency]]:
        """
        Get a dictionary with all exchange tokens and chains where they can be withdrawn.

        Args:
            token_symbol (Optional[str]): single or multiple token symbols (no more than 20) separated with comma,
                e.g. BTC or BTC,ETH. (absolutely all)

        Returns:
            Dict[str, Dict[str, Currency]]: the dictionary with all exchange tokens and chains where they can be
                withdrawn.

        """
        method = 'currencies'
        body = {
            'ccy': token_symbol
        }
        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        currencies = {}
        for currency in response.get('data'):
            token_symbol = currency.get('ccy')
            chain = '-'.join(currency.get('chain').split('-')[1:])
            if token_symbol not in currencies:
                currencies[token_symbol] = {}

            if chain not in currencies[token_symbol]:
                currencies[token_symbol][chain] = Currency(data=currency)

        return currencies

    async def balances(self, token_symbol: Optional[str] = None) -> Dict[str, FundingToken]:
        """
        Get a dictionary with tokens and their balances in the funding account.

        Args:
            token_symbol (Optional[str]): single or multiple token symbols (no more than 20) separated with comma,
                e.g. BTC or BTC,ETH. (absolutely all)

        Returns:
            Dict[str, FundingToken]: the dictionary with tokens and their balances in the funding account.

        """
        method = 'balances'
        body = {
            'ccy': token_symbol
        }
        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        tokens = {}
        for token in response.get('data'):
            tokens[token.get('ccy')] = FundingToken(data=token)

        return tokens

    async def deposit_history(
            self, token_symbol: Optional[str] = None, depId: Optional[Union[str, int]] = None,
            fromWdId: Optional[Union[str, int]] = None, txId: Optional[str] = None,
            type: Optional[TransactionType] = None, state: Optional[DepositStatus] = None,
            after: Optional[int] = None, before: Optional[int] = None, limit: int = 100
    ) -> Dict[int, Deposit]:
        """
        Get a dictionary with deposit IDs and information about deposits.

        Args:
            token_symbol (Optional[str]): token symbol, e.g. BTC. (absolutely all)
            depId (Optional[Union[str, int]]): deposit ID. (None)
            fromWdId (Optional[Union[str, int]]): internal transfer initiator's withdrawal ID. If the deposit comes
                from internal transfer, this field displays the withdrawal ID of the internal transfer initiator. (None)
            txId (Optional[str]): hash record of the deposit. (None)
            type (Optional[TransactionType]): deposit type. (absolutely all)
            state (Optional[DepositStatus]): status of deposit. (absolutely all)
            after (Optional[int]): pagination of data to return records earlier than the requested ts,
                Unix timestamp format in milliseconds, e.g. 1654041600000. (None)
            before (Optional[int]): Pagination of data to return records newer than the requested ts,
                Unix timestamp format in milliseconds, e.g. 1656633600000. (None)
            limit (int): number of results per request, the maximum is 100. (100)

        Returns:
            Dict[int, Deposit]: the dictionary with deposit IDs and information about deposits.

        """
        method = 'deposit-history'
        body = {
            'ccy': token_symbol,
            'depId': str(depId) if depId else None,
            'fromWdId': str(fromWdId) if fromWdId else None,
            'txId': txId,
            'type': type.state if type else None,
            'state': state.state if state else None,
            'limit': limit
        }

        if after:
            body['after'] = secs_to_millisecs(secs=after)

        if before:
            body['before'] = secs_to_millisecs(secs=before)

        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        deposits = {}
        for deposit in response.get('data'):
            deposits[int(deposit.get('depId'))] = Deposit(data=deposit)

        return deposits

    async def withdrawal_history(
            self, token_symbol: Optional[str] = None, wdId: Optional[Union[str, int]] = None,
            clientId: Optional[Union[str, int]] = None, txId: Optional[str] = None,
            type: Optional[TransactionType] = None, state: Optional[WithdrawalStatus] = None,
            after: Optional[int] = None, before: Optional[int] = None, limit: int = 100
    ) -> Dict[int, Withdrawal]:
        """
        Get a dictionary with withdrawal IDs and information about withdrawals.

        Args:
            token_symbol (Optional[str]): token symbol, e.g. BTC. (absolutely all)
            wdId (Optional[Union[str, int]]): withdrawal ID. (None)
            clientId (Optional[Union[str, int]]): client-supplied ID. (None)
            txId (Optional[str]): hash record of the withdrawal. (None)
            type (Optional[TransactionType]): withdrawal type. (absolutely all)
            state (Optional[WithdrawalStatus]): status of withdrawal. (absolutely all)
            after (Optional[int]): pagination of data to return records earlier than the requested ts,
                Unix timestamp format in milliseconds, e.g. 1654041600000. (None)
            before (Optional[int]): pagination of data to return records newer than the requested ts,
                Unix timestamp format in milliseconds, e.g. 1656633600000. (None)
            limit (int): number of results per request, the maximum is 100. (100)

        Returns:
            Dict[int, Withdrawal]: the dictionary with withdrawal IDs and information about withdrawals.

        """
        method = 'withdrawal-history'
        body = {
            'ccy': token_symbol,
            'wdId': str(wdId) if wdId else None,
            'clientId': str(clientId) if clientId else None,
            'txId': txId,
            'type': type.state if type else None,
            'state': state.state if state else None,
            'limit': limit
        }

        if after:
            body['after'] = await secs_to_millisecs(secs=after)

        if before:
            body['before'] = await secs_to_millisecs(secs=before)

        response = await self.make_request(
            method=Methods.GET, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        withdrawals = {}
        for withdrawal in response.get('data'):
            withdrawals[int(withdrawal.get('wdId'))] = Withdrawal(data=withdrawal)

        return withdrawals

    async def withdrawal(
            self, token_symbol: str, amount: Union[float, int, str], toAddr: str, chain: str,
            dest: TransactionType = TransactionTypes.OnChain, fee: Optional[Union[float, int, str]] = None,
            areaCode: Union[int, str] = None, clientId: Optional[Union[str, int]] = None
    ) -> WithdrawalToken:
        """
        Withdraw funds from the funding account.

        Args:
            token_symbol (str): token symbol, e.g. USDT.
            amount (Union[float, int, str]): withdrawal amount.
            toAddr (str): if your dest is 4,toAddr should be a trusted crypto currency address. Some crypto currency
                addresses are formatted as 'address:tag', e.g. 'ARDOR-7JF3-8F2E-QUWZ-CAN7F:123456'. If your dest is 3,
                toAddr should be a recipient address which can be email, phone or login account name.
            chain (str): chain name.
            dest (TransactionType): withdrawal method. (on-chain)
            fee (Union[float, int, str]): transaction fee. (minimal, parsed using the 'currencies' function)
            areaCode (Optional[str]): area code for the phone number. If toAddr is a phone number, this parameter is
                required. (None)
            clientId (Optional[Union[str, int]]): Client-supplied ID. A combination of case-sensitive alphanumerics,
                all numbers, or all letters of up to 32 characters. (None)

        Returns:
            WithdrawalToken: an instance with information about the withdrawal.

        """
        method = 'withdrawal'
        if not fee:
            currency = await self.currencies(token_symbol=token_symbol)
            fee = currency[token_symbol][chain].minFee

        body = {
            'ccy': token_symbol,
            'amt': str(amount),
            'dest': dest.state,
            'toAddr': toAddr,
            'fee': str(fee),
            'chain': chain if token_symbol in chain else f'{token_symbol}-{chain}',
            'areaCode': str(areaCode) if areaCode else None,
            'clientId': str(clientId) if clientId else None
        }
        response = await self.make_request(
            method=Methods.POST, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        return WithdrawalToken(data=response.get('data')[0])

    async def cancel_withdrawal(self, wdId: Union[str, int]) -> int:
        """
        Cancel a withdrawal.

        Args:
            wdId (Optional[Union[str, int]]): withdrawal ID.

        Returns:
            int: the withdrawal ID.

        """
        method = 'cancel-withdrawal'
        body = {
            'wdId': str(wdId)
        }
        response = await self.make_request(
            method=Methods.POST, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        return int(response.get('data')[0]['wdId'])

    async def transfer(
            self, token_symbol: str, amount: Union[float, int, str], from_: AccountType = AccountTypes.Funding,
            to_: AccountType = AccountTypes.Trading, subAcct: Optional[str] = None,
            type: TransferType = TransferTypes.WithinAccount, loanTrans: bool = False,
            clientId: Optional[Union[str, int]] = None, omitPosRisk: bool = False
    ) -> Transfer:
        """
        Transfer tokens within account or between sub-accounts.

        Args:
            token_symbol (str): token symbol, e.g. USDT.
            amount (Union[float, int, str]): amount to be transferred.
            from_ (AccountType): the remitting account. (funding)
            to_ (AccountType): the beneficiary account. (trading)
            subAcct (str): name of the sub-account. When 'type' is 1, 2 or 4, sub-account is required. (None)
            type (TransferType): transfer type. (within account)
            loanTrans (bool): whether borrowed coins can be transferred out under Multi-currency margin
                and Portfolio margin. (False)
            clientId (Optional[Union[str, int]]): client-supplied ID. A combination of case-sensitive alphanumerics,
                all numbers, or all letters of up to 32 characters. (None)
            omitPosRisk (bool): ignore position risk. Applicable to Portfolio margin. (False)

        Returns:
            TransferredToken: an instance with information about the transfer.

        """
        method = 'transfer'
        body = {
            'ccy': token_symbol,
            'amt': str(amount),
            'from_': from_.state,
            'to_': to_.state,
            'subAcct': subAcct,
            'type': type.state,
            'loanTrans': loanTrans,
            'clientId': str(clientId) if clientId else None,
            'omitPosRisk': omitPosRisk
        }
        response = await self.make_request(
            method=Methods.POST, request_path=f'/api/v5/{self.section}/{method}', body=aiohttp_params(body)
        )
        return Transfer(data=response.get('data')[0])
