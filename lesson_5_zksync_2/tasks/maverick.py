'''
eth -> usdc (0.001): https://explorer.zksync.io/tx/0x4ab60213c10d57af851e1832238b524a2552dcaa4f6c13b1e3e3f20f93451290
usdc -> eth: https://explorer.zksync.io/tx/0x33c47dce5f132d842416d4ed70fe7346a307215ed6aa3eb5ed10ce22e221f503
'''

import logging
import time

from web3 import Web3
from web3.types import HexStr
from eth_async.models import TokenAmount, RawContract
from web3.types import TxParams

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
                ...
            ],
    }
    PATH_MAP_SELL = {
        'USDC': [
                Web3.to_bytes(hexstr=HexStr(Contracts.USDC.address)),
                Web3.to_bytes(hexstr=HexStr('57681331b6cb8df134dccb4b54dc30e8fcdf0ad8')),
                Web3.to_bytes(hexstr=HexStr(Contracts.WETH.address)),
            ],
        'BUSD': [
                ...
            ],
    }

    async def _swap_eth_to_token(
            self,
            amount: TokenAmount,
            to_token: RawContract,
            slippage: float = 1.0
    ) -> str:
        to_token_address = Web3.to_checksum_address(to_token.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        path = self.PATH_MAP_BUY[to_token_name]

        from_token_address = Web3.to_checksum_address(path[0])
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        failed_text = f'Failed to swap {from_token_name} to {to_token_name} via Maverick'

        contract = await self.client.contracts.get(contract_address=Contracts.MAVERICK)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        deadline = int(time.time() + 20 * 60)
        encoded_path = b''.join(path)

        # exactInput params (path, recipient, deadline, amount, minAcquired)
        swap_amount_args = (
            encoded_path,
            f'{self.client.account.address}',
            deadline,
            amount.Wei,
            amount_out_min.Wei,
        )
        swap_amount_data = contract.encodeABI('exactInput', args=[swap_amount_args])

        # refundETH params (None)
        return_eth_data = contract.encodeABI('refundETH', args=[])

        # multicall params (data)
        swap_data = contract.encodeABI(
            'multicall',
            args=[
                [swap_amount_data, return_eth_data]
            ]
        )

        tx_params = TxParams(
            to=contract.address,
            data=swap_data,
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via Maverick: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            slippage: float = 1.
    ) -> str:
        return await self._swap_eth_to_token(
            amount=amount,
            to_token=Contracts.USDC,
            slippage=slippage
        )

    # async def swap_eth_to_busd(self) -> str:
    #     return await self.swap_eth(token_to=Contracts.BUSD)

    # async def swap_token_usdc_to_eth(self) -> str:
    #     return await self.swap_token(token_from=Contracts.USDC)

    # async def swap_token_busd_to_eth(self) -> str:
    #     return await self.swap_token(token_from=Contracts.BUSD)
