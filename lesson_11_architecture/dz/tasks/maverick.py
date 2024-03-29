'''
eth -> usdc (0.001): https://explorer.zksync.io/tx/0x4ab60213c10d57af851e1832238b524a2552dcaa4f6c13b1e3e3f20f93451290
usdc -> eth: https://explorer.zksync.io/tx/0x33c47dce5f132d842416d4ed70fe7346a307215ed6aa3eb5ed10ce22e221f503

usdc -> eth https://explorer.zksync.io/tx/0xed5702d43f4bc1eead2704e3327c0ead65691d0721c11680cb5ae20b5e7076ba
'''

import time
import asyncio
import random

from web3 import Web3
from web3.types import HexStr
from web3.types import TxParams
from loguru import logger

from libs.eth_async.data.models import TokenAmount
from data.models import Contracts
from tasks.base import Base


class Maverick(Base):
    PATH_MAP_BUY = {
        'USDC': [
                Web3.to_bytes(hexstr=HexStr(Contracts.WETH.address)),
                Web3.to_bytes(hexstr=HexStr('41c8cf74c27554a8972d3bf3d2bd4a14d8b604ab')),
                Web3.to_bytes(hexstr=HexStr(Contracts.USDC.address)),
            ],
        'BUSD': [
                Web3.to_bytes(hexstr=HexStr(Contracts.WETH.address)),
                Web3.to_bytes(hexstr=HexStr('57681331b6cb8df134dccb4b54dc30e8fcdf0ad8')),
                Web3.to_bytes(hexstr=HexStr(Contracts.USDC.address)),
                Web3.to_bytes(hexstr=HexStr('e799043fb52ff46cc57ce8a8b1ac3f151ba270f7')),
                Web3.to_bytes(hexstr=HexStr(Contracts.ceBUSD.address))
            ],
    }
    PATH_MAP_SELL = {
        'USDC': [
                Web3.to_bytes(hexstr=HexStr(Contracts.USDC.address)),
                Web3.to_bytes(hexstr=HexStr('57681331b6cb8df134dccb4b54dc30e8fcdf0ad8')),
                Web3.to_bytes(hexstr=HexStr(Contracts.WETH.address)),
            ],
        'BUSD': [
                Web3.to_bytes(hexstr=HexStr(Contracts.ceBUSD.address)),
                Web3.to_bytes(hexstr=HexStr('3ae63fb198652e294b8de4c2ef659d95d5ff28be')),
                Web3.to_bytes(hexstr=HexStr(Contracts.WETH.address)),
            ],
    }

    async def _swap(
            self,
            amount: TokenAmount,
            path: list[bytes],
            slippage: float = 1.0
    ) -> str:
        to_token_address = Web3.to_checksum_address(path[-1])
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        from_token_address = Web3.to_checksum_address(path[0])
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        from_token_is_eth = from_token.address.upper() == Contracts.WETH.address.upper()

        failed_text = f'Failed to swap {from_token_name} to {to_token_name} via Maverick'
        logger.info(f'Start to swap {from_token_name} to {to_token_name} via Maverick')

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        contract = await self.client.contracts.get(contract_address=Contracts.MAVERICK)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        if not from_token_is_eth:
            if await self.approve_interface(
                    token_address=from_token.address,
                    spender=contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'

        deadline = int(time.time() + 20 * 60)
        encoded_path = b''.join(path)

        # exactInput params (path, recipient, deadline, amount, minAcquired)
        if from_token_is_eth:
            swap_amount_args = (
                encoded_path,
                f'{self.client.account.address}',
                deadline,
                amount.Wei,
                amount_out_min.Wei,
            )
        else:
            swap_amount_args = (
                encoded_path,
                '0x0000000000000000000000000000000000000000',
                deadline,
                amount.Wei,
                amount_out_min.Wei,
            )
        swap_amount_data = contract.encodeABI('exactInput', args=[swap_amount_args])

        if from_token_is_eth:
            second_item = contract.encodeABI('refundETH', args=[])
        else:
            second_item = contract.encodeABI('unwrapWETH9', args=[
                amount_out_min.Wei,
                f'{self.client.account.address}',
            ])

        # multicall params (data)
        swap_data = contract.encodeABI(
            'multicall',
            args=[
                [swap_amount_data, second_item]
            ]
        )

        tx_params = TxParams(
            to=contract.address,
            data=swap_data,
            value=amount.Wei if from_token_is_eth else 0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via Maverick: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.
    ) -> str:
        if not amount:
            amount = Base.get_eth_amount_for_swap()
        return await self._swap(
            amount=amount,
            path=Maverick.PATH_MAP_BUY['USDC'],
            slippage=slippage
        )

    async def swap_eth_to_busd(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.
    ) -> str:
        if not amount:
            amount = Base.get_eth_amount_for_swap()
        return await self._swap(
            amount=amount,
            path=Maverick.PATH_MAP_BUY['BUSD'],
            slippage=slippage
        )

    async def swap_usdc_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.
    ) -> str:
        return await self._swap(
            amount=amount,
            path=Maverick.PATH_MAP_SELL['USDC'],
            slippage=slippage
        )

    async def swap_busd_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.
    ) -> str:
        return await self._swap(
            amount=amount,
            path=Maverick.PATH_MAP_SELL['BUSD'],
            slippage=slippage
        )
