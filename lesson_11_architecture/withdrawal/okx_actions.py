from loguru import logger
from decimal import Decimal

from libs.py_okx_async.OKXClient import OKXClient
from libs.py_okx_async.asset.models import TransferTypes, Currency, Withdrawal
from libs.py_okx_async.exceptions import APIException
from libs.py_okx_async.models import OKXCredentials, Chains, AccountTypes

from data.models import Settings


class OKXActions:
    def __init__(self, credentials: OKXCredentials):
        self.entrypoint_url = 'https://www.okx.com'
        self.credentials = credentials
        self.okx_client = None
        if self.credentials.completely_filled():
            self.okx_client = OKXClient(credentials=credentials, entrypoint_url=self.entrypoint_url)

    async def all_balances_are_zero(self) -> bool:
        for subaccount_name in await self.okx_client.subaccount.list():
            balances = await self.okx_client.subaccount.asset_balances(subAcct=subaccount_name, token_symbol='ETH')
            for balance in balances.values():
                avail_bal = balance.availBal
                if avail_bal > 0:
                    return False
        return True

    async def collect_funds_from_subaccounts(self):
        for subaccount_name in await self.okx_client.subaccount.list():
            balances = await self.okx_client.subaccount.asset_balances(subAcct=subaccount_name, token_symbol='ETH')
            for balance in balances.values():
                avail_bal = balance.availBal
                if avail_bal > 0:
                    await self.okx_client.asset.transfer(
                        token_symbol='ETH', amount=avail_bal, to_=AccountTypes.Funding, subAcct=subaccount_name,
                        type=TransferTypes.SubToMasterMasterKey
                    )

    async def get_master_acc_balance(self, token_symbol: str = 'ETH') -> float | int:
        master_acc_balance = await self.okx_client.asset.balances(token_symbol)
        return master_acc_balance[token_symbol].availBal

    async def get_subaccounts_frozen_balances(self):
        total_frozen_bal = 0
        for subaccount_name in await self.okx_client.subaccount.list():
            balances = await self.okx_client.subaccount.asset_balances(subAcct=subaccount_name, token_symbol='ETH')
            for balance in balances.values():
                frozen_bal = balance.frozenBal
                if frozen_bal > 0:
                    total_frozen_bal += frozen_bal
        return total_frozen_bal

    async def get_withdrawal_fee(self, token_symbol: str, chain: str) -> float | None:
        token_symbol = token_symbol.upper()
        currencies = await self.okx_client.asset.currencies(token_symbol=token_symbol)
        if token_symbol not in currencies:
            return None

        currency = currencies[token_symbol]
        if chain not in currency:
            return None

        currency_info: Currency = currency[chain]
        if not currency_info.canWd:
            return None

        if currency_info.minFee:
            return currency_info.minFee
        return None

    async def try_to_get_tx_hash(self, wd_id: str | int) -> str | None:
        wd_id = int(wd_id)
        withdrawal_history = await self.okx_client.asset.withdrawal_history(wdId=wd_id)
        if withdrawal_history and withdrawal_history.get(wd_id) and withdrawal_history.get(wd_id).txId:
            return withdrawal_history.get(wd_id).txId

    async def withdraw(
            self,
            to_address: str,
            amount: float | int | str,
            token_symbol: str = 'APT',
            chain: str = Chains.Aptos,
    ) -> str:
        failed_text = 'Failed to withdraw from OKX'
        try:
            if not self.okx_client:
                return f'{failed_text}: there is no okx_client'

            fee = await self.get_withdrawal_fee(token_symbol=token_symbol, chain=chain)
            fee = str(Decimal(str(fee)))

            if not fee:
                return f'{failed_text} | can not get fee for withdraw'
            withdrawal_token = await self.okx_client.asset.withdrawal(
                token_symbol=token_symbol, amount=amount, toAddr=to_address, fee=fee, chain=chain
            )
            withdrawal_id = withdrawal_token.wdId
            if withdrawal_id:
                return f'A withdrawal request of {amount} {token_symbol} was sent: ({withdrawal_id}) to {to_address}'

            return f'{failed_text}!'
        except APIException as e:
            logger.error(f'{to_address} | {e}')
            return f'{failed_text}: {e}'
        except BaseException as e:
            logger.exception(f'withdraw: {e}')
            return f'{failed_text}: {e}'

    async def check_withdrawal_status(
            self,
            settings: Settings,
            to_address: str,
            chain: str = Chains.Starknet,
    ) -> bool | None:
        withdrawls_txs = await self.okx_client.asset.withdrawal_history(
            token_symbol='ETH',
            before=settings.volume.timestamp
        )

        for wdId in withdrawls_txs:
            tx: Withdrawal = withdrawls_txs[wdId]
            if tx.chain == chain and tx.to_ == to_address:
                if int(tx.state.state) == 2:
                    return True
                else:
                    return False

        return False
