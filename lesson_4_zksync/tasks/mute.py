'''
eth -> usdc (0.0015): https://explorer.zksync.io/tx/0xddf9fa912606b997dff68193f0393728f3a962d084d78a7d812571dc9890f22b
usdc -> eth: https://explorer.zksync.io/tx/0x375c3a6cab8d55465bbbdf907f5483c80499ef18592a77c1d7373cc6ba6ac5e0
'''

import time
import asyncio
import random
from web3.types import TxParams

from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount
from data.models import Contracts


class Mute(Base):
    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            slippage: float = 1.,
    ) -> str:
        to_token = Contracts.USDC

        to_token = await self.client.contracts.default_token(contract_address=to_token.address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap ETH to {to_token_name} via Mute'

        contract = await self.client.contracts.get(contract_address=Contracts.MUTE)

        eth_price = await self.get_token_price(token_symbol='ETH')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * eth_price * (1 - slippage / 100),
            decimals=await self.client.transactions.get_decimals(contract=to_token.address)
        )

        params = TxArgs(
            amountOutMin=amount_out_min.Wei,
            path=[Contracts.WETH.address, to_token.address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60),
            stable=[False, False],
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactETHForTokensSupportingFeeOnTransferTokens', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} ETH was swapped to {to_token_name} via Mute: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_usdc_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.
    ) -> str:
        from_token = await self.client.contracts.default_token(contract_address=Contracts.USDC.address)
        from_token_name = await from_token.functions.symbol().call()
        failed_text = f'Failed swap ETH to {from_token_name} via Mute'

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)
            if not amount.Wei:
                return f'{failed_text}: {self.client.account.address} | Mute | swap_token | ' \
                       f'not enough {from_token_name} balance ({amount.Ether})'

        contract = await self.client.contracts.get(contract_address=Contracts.MUTE)

        if await self.approve_interface(
                token_address=from_token.address,
                spender=contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        eth_price = await self.get_token_price(token_symbol='ETH')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) / eth_price * (1 - slippage / 100),
        )

        params = TxArgs(
            amountIn=amount.Wei,
            amountOutMin=amount_out_min.Wei,
            path=[from_token.address, Contracts.WETH.address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60),
            stable=[False, False],
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactTokensForETHSupportingFeeOnTransferTokens', args=params.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to ETH via Mute: {tx.hash.hex()}'
        return f'{failed_text}!'
