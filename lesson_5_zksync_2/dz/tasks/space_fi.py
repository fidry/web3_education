'''
eth -> usdc (0.001): https://explorer.zksync.io/tx/0xac1acb194970bb3c796a8b06c5d21a365b8b6be7408babe4b8f3218e3af28f08
eth -> usdc (0.0015): https://explorer.zksync.io/tx/0x55cc113c631972e2b639cebe811a92b834179dbb0c5433625788a81cae523ffd
usdc -> eth: https://explorer.zksync.io/tx/0x9572a59bad67c172cc19b5d9e4159fca079ddf4d5aa44eaac46a3b0ff535d77d

сигнатуры: https://www.4byte.directory/
'''

import time
import asyncio
import random

from web3.types import TxParams
from web3 import Web3

from tasks.base import Base
from eth_async.models import RawContract, TxArgs, TokenAmount
from data.models import Contracts


# SpaceFiABI = [
#     {
#         'constant': False,
#         'inputs': [
#             {'name': 'amountOut', 'type': 'uint256'},
#             {'name': 'path', 'type': 'address[]'},
#             {'name': 'toAddress', 'type': 'address'},
#             {'name': 'deadline', 'type': 'uint256'},
#         ],
#         'name': 'no_name',
#         'outputs': [],
#         'payable': False,
#         'stateMutability': 'nonpayable',
#         'type': 'function'
#     }
# ]


class SpaceFi(Base):
    async def _swap(
            self,
            path: list[str],
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        from_token_address = Web3.to_checksum_address(path[0])
        to_token_address = Web3.to_checksum_address(path[-1])
        from_token_is_eth = from_token_address.upper() == Contracts.WETH.address.upper()

        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via SpaceFi'

        contract = await self.client.contracts.get(contract_address=Contracts.SPACE_FI)

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
            '''
            0x7ff36ab5
            0000000000000000000000000000000000000000000000000000000000038253 - amountOut
            0000000000000000000000000000000000000000000000000000000000000080 - array link
            000000000000000000000000b7a4557a2bbd392a89fbe80aa726cbd645d112cb - account address
            0000000000000000000000000000000000000000000000000000000065c218a7 - deadline
            0000000000000000000000000000000000000000000000000000000000000002 - array size
            0000000000000000000000005aea5775959fbc2557cc8789bc1bf90a239d9a91 - WETH
            0000000000000000000000003355df6d4c9c3035724fd0e3914de96a5a83aaf4 - USDC
            '''

            data = (
                f'0x7ff36ab5'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"80".zfill(64)}'
                f'{str(self.client.account.address).lower()[2:].zfill(64)}'
                f'{hex(int(time.time()) + 20 * 60)[2:].zfill(64)}'
                f'{hex(len(path))[2:].zfill(64)}'
            )
            for p in path:
                data += p[2:].lower().zfill(64)

            # params = TxArgs(
            #     amountOut=amount_out_min.Wei,
            #     path=path,
            #     toAddress=self.client.account.address,
            #     deadline=int(time.time() + 20 * 60),
            # )

        else:
            params = TxArgs(
                amountIn=amount.Wei,
                amountOutMin=amount_out_min.Wei,
                path=path,
                to=self.client.account.address,
                deadline=int(time.time() + 20 * 60),
            )

        function_name = 'swapExactETHForTokens' if from_token_is_eth \
            else 'swapExactTokensForETH'

        tx_params = TxParams(
            to=contract.address,
            # data=contract.encodeABI(function_name, args=params.tuple()),
            data=data,
            value=amount.Wei if from_token_is_eth else 0
        )

        # self.parse_params(params=tx_params['data'])

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via SpaceFi: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.USDC.address],
            slippage=slippage
        )

    async def swap_eth_to_usdt(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.USDT.address],
            slippage=slippage
        )

    async def swap_eth_to_busd(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.ceBUSD.address],
            slippage=slippage
        )

    async def swap_eth_to_wbtc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.WBTC.address],
            slippage=slippage
        )

    async def swap_busd_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.ceBUSD.address, Contracts.WETH.address],
            slippage=slippage
        )

    async def swap_usdt_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        return await self._swap(
            amount=amount,
            path=[Contracts.USDT.address, Contracts.USDC.address, Contracts.WETH.address],
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
            path=[Contracts.WBTC.address, Contracts.USDC.address, Contracts.WETH.address],
            slippage=slippage
        )
