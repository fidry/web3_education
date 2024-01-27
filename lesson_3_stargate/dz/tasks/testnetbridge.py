from typing import Optional
import random

from web3.types import TxParams

from data.models import Contracts
from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount, Networks


class Testnetbridge(Base):
    async def swap_geth(
            self,
            geth_amount: Optional[TokenAmount] = None,
            max_fee: float = 1
    ) -> str:
        failed_text = 'Failed to send GETH via TestnetBridge'

        if self.client.network.name != Networks.Arbitrum.name:
            return f'{failed_text}: wrong network ({self.client.network.name})'

        if not geth_amount:
            geth_amount = self.client.wallet.balance(Contracts.ARBITRUM_GETH)

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_TESTNETBRIDGE)

        geth_balance = await self.client.wallet.balance(token=Contracts.ARBITRUM_GETH)
        if geth_balance.Wei <= 0:
            return f'{failed_text}: to low GETH balance'

        # fee = TokenAmount(
        #     amount=random.randint(60000000000000, 70000000000000),
        #     wei=True
        # )
        fee = await self.get_value(amount=geth_amount)

        token_price = await self.get_token_price(token_symbol=self.client.network.coin_symbol)
        fee_dollar = float(fee.Ether) * token_price
        if fee_dollar > max_fee:
            return f'{failed_text}: {self.client.account.address} | too high fee | {fee_dollar}$'

        args = TxArgs(
            _from=self.client.account.address,
            _dstChainId=154,
            _toAddress=str(self.client.account.address),
            _amount=geth_amount.Wei,
            _refundAddress=self.client.account.address,
            _zroPaymentAddress='0x0000000000000000000000000000000000000000',
            _adapterParams='0x'
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('sendFrom', args=args.tuple()),
            value=fee.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{geth_amount.Ether} GETH send via TestnetBridge: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def get_value(self, amount: TokenAmount) -> Optional[TokenAmount]:
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_TESTNETBRIDGE)
        res = await contract.functions.estimateSendFee(
            154,
            self.client.account.address,
            amount.Wei,
            False,
            '0x'
        ).call()
        return TokenAmount(amount=int(res[0]), wei=True)
