'''
eth -> usdc (0.0015): https://explorer.zksync.io/tx/0xddf9fa912606b997dff68193f0393728f3a962d084d78a7d812571dc9890f22b
usdc -> eth: https://explorer.zksync.io/tx/0x375c3a6cab8d55465bbbdf907f5483c80499ef18592a77c1d7373cc6ba6ac5e0
'''

import time
import asyncio
import random
from web3.types import TxParams
from web3 import Web3
from loguru import logger

from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts


class Mute(Base):
    async def _swap(
            self,
            path: list[str],
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ):
        from_token_address = Web3.to_checksum_address(path[0])
        to_token_address = Web3.to_checksum_address(path[-1])

        from_token_is_eth = from_token_address.upper() == Contracts.WETH.address.upper()

        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Mute'
        logger.info(f'Start to swap {from_token_name} to {to_token_name} via Mute')

        contract = await self.client.contracts.get(contract_address=Contracts.MUTE)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        if not from_token_is_eth:
            if await self.approve_interface(
                    token_address=from_token.address,
                    spender=contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        if from_token_is_eth:
            params = TxArgs(
                amountOutMin=amount_out_min.Wei,
                path=path,
                to=self.client.account.address,
                deadline=int(time.time() + 20 * 60),
                stable=[False, False],
            )
        else:
            params = TxArgs(
                amountIn=amount.Wei,
                amountOutMin=amount_out_min.Wei,
                path=path,
                to=self.client.account.address,
                deadline=int(time.time() + 20 * 60),
                stable=[False, False],
            )

        function_name = 'swapExactETHForTokensSupportingFeeOnTransferTokens' if from_token_is_eth \
            else 'swapExactTokensForETHSupportingFeeOnTransferTokens'

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI(function_name, args=params.tuple()),
            value=amount.Wei if from_token_is_eth else 0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via Mute: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        if not amount:
            amount = Base.get_eth_amount_for_swap()
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.USDC.address],
            slippage=slippage
        )

    async def swap_eth_to_wbtc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        if not amount:
            amount = Base.get_eth_amount_for_swap()
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.WBTC.address],
            slippage=slippage
        )

    async def swap_usdc_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.USDC.address, Contracts.WETH.address],
            slippage=slippage
        )

    async def swap_wbtc_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.WBTC.address, Contracts.WETH.address],
            slippage=slippage
        )
