'''
eth -> usdc (0.001): https://explorer.zksync.io/tx/0x4d2215efd2a054fa4d0d0f40d3d7b73006613d955ff55b8e80b1b883af8ba006
usdc -> eth: https://explorer.zksync.io/tx/0x4dbbe7154c3f164dfab0dfeb3d2f31f25668d49b4dd6258b0234b26179d3f9b8
'''

from eth_async.models import Network, Networks, RawContract, DefaultABIs
import time
from web3.types import TxParams
from web3 import Web3

from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount

from data.models import Contracts


class SyncSwap(Base):
    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            slippage: float = 1.0
    ) -> str:

        to_token = Contracts.USDC

        to_token = await self.client.contracts.default_token(contract_address=to_token.address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap ETH to {to_token_name} via SyncSwap'

        contract = await self.client.contracts.get(contract_address=Contracts.SYNC_SWAP)

        eth_price = await self.get_token_price(token_symbol='ETH')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * eth_price * (1 - slippage / 100),
            decimals=await self.client.transactions.get_decimals(contract=to_token)
        )

        pool = Web3.to_checksum_address('0x80115c708e12edd42e504c1cd52aea96c547c05c')

        params = TxArgs(
            paths=[
                TxArgs(
                    steps=[
                        TxArgs(
                            pool=pool,
                            data=f'0x{Contracts.WETH.address[2:].zfill(64)}'
                                 f'{str(self.client.account.address)[2:].zfill(64)}'
                                 f'{"2".zfill(64)}',
                            callback='0x0000000000000000000000000000000000000000',
                            callbackData='0x'
                        ).tuple(),
                    ],
                    tokenIn='0x0000000000000000000000000000000000000000',
                    amountIn=amount.Wei
                ).tuple(),
            ],
            amountOutMin=amount_out_min.Wei,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=params.tuple()),
            value=amount.Wei
        )

        # self.parse_params(tx_params['data'])

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} ETH was swapped to {to_token_name} via SyncSwap: {tx.hash.hex()}'
        return f'{failed_text}!'
