'''
bsc -> coredao: https://bscscan.com/tx/0xe8223775f9fda4610d373dd70453b6755ce4f99a1d810168a5da81a090efed39
'''

import asyncio
import random
from web3.types import TxParams

from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount, Networks

from data.models import Contracts


class CoredaoBridge(Base):
    async def bridge_usdt_bsc_to_usdt_coredao(self, amount: TokenAmount | None = None, max_fee: float = 1):
        failed_text = 'Failed to send USDT (bsc) to USDT (coredao) via CoredaoBridge'

        if self.client.network.name != Networks.BSC.name:
            return f'{failed_text}: wrong network ({self.client.network.name})'

        usdt_balance = await self.client.wallet.balance(token=Contracts.BSC_USDT)
        if not amount:
            amount = usdt_balance

        if usdt_balance.Wei < amount.Wei:
            return (f'{failed_text}: {self.client.account.address} | '
                    f'not enough balance ({usdt_balance.Ether} / {amount.Ether})')

        contract = await self.client.contracts.get(contract_address=Contracts.BSC_COREDAO_BRIDGE)

        fee = await self.get_value_bsc_coredao()
        token_price = await self.get_token_price(token_symbol=self.client.network.coin_symbol)
        fee_dollar = float(fee.Ether) * token_price
        if fee_dollar > max_fee:
            return f'{failed_text}: {self.client.account.address} too high fee | {fee_dollar}$'

        bsc_balance = await self.client.wallet.balance()
        if bsc_balance.Wei < fee.Wei:
            return (f'{failed_text}: {self.client.account.address} '
                    f'not enought native token | balance: {bsc_balance.Ether} | fee: {fee.Ether}')

        if await self.approve_interface(
                token_address=Contracts.BSC_USDT.address,
                spender=contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        args = TxArgs(
            token=Contracts.BSC_USDT.address,
            amountLD=amount.Wei,
            to=self.client.account.address,
            callParams=TxArgs(
                refundAddress=self.client.account.address,
                zroPaymentAddress='0x0000000000000000000000000000000000000000'
            ).tuple(),
            adapterParams='0x'
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('bridge', args=args.tuple()),
            value=fee.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} USDT was send to Coredao via CoredaoBridge: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def get_value_bsc_coredao(self) -> TokenAmount:
        contract = await self.client.contracts.get(contract_address=Contracts.BSC_COREDAO_BRIDGE)
        res = await contract.functions.estimateBridgeFee(
            False,
            '0x'
        ).call()
        return TokenAmount(amount=res[0], wei=True)
