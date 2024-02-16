'''
eth -> usdt: https://starkscan.co/tx/0x07d41f252cce989ce877b04a171c2af853cdbb287115902941098b7fcaf56193
usdt -> eth: https://starkscan.co/tx/0x01e235214c4e1f96bb20aa7ed2979042e2565a8dd36f043d19d7b1752ec236bc
'''

import time

from starknet_py.contract import Contract

from data import models
from tasks.base import Base
from data.models import TokenAmount, DEFAULT_TOKEN_ABI


class Swap10K(Base):
    NAME = '10kSwap'
    AVAILABLE_SWAP = ['USDC', 'DAI', 'USDT', 'WBTC']
    CONTRACT_MAP = {
        'USDC': {
            'token_address': models.USDC_ADDRESS,
        },
        'DAI': {
            'token_address': models.DAI_ADDRESS,
        },
        'USDT': {
            'token_address': models.USDT_ADDRESS,
        },
        'WBTC': {
            'token_address': models.WBTC_ADDRESS,
        }
    }

    async def swap_eth_to_token(self, amount_in: TokenAmount, token_name: str):
        """ Swap ETH to USDC/DAI/USDT/WBTC """

        token_name = token_name.upper()
        failed_text = f'Failed swap ETH to {token_name} via 10kswap'
        try:
            eth_contract = Contract(
                address=models.ETH_ADDRESS,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account
            )

            token_address = Swap10K.CONTRACT_MAP[token_name]['token_address']
            token_out_decimal = await self.starknet_client.get_decimals(token_address)

            amount_out = await Base.get_amount_out(
                amount_in=amount_in,
                token_in_name='ETH',
                token_out_name=token_name,
                amount_out_decimals=token_out_decimal
            )

            swap10k_contract = await Contract.from_address(
                address=models.SWAP10K_ROUTER,
                provider=self.starknet_client.account,
            )

            approve_call = eth_contract.functions["approve"].prepare_call(
                spender=models.SWAP10K_ROUTER,
                amount=amount_in.Wei
            )

            swap_call = swap10k_contract.functions["swapExactTokensForTokens"].prepare_call(
                amountIn=amount_in.Wei,
                amountOutMin=amount_out.Wei,
                path=[
                    models.ETH_ADDRESS,
                    token_address
                ],
                to=self.starknet_client.account.address,
                deadline=int(time.time() + 20 * 60)
            )

            response = await self.starknet_client.account.execute_v1(
                calls=[approve_call, swap_call],
                auto_estimate=True
            )

            decimal_value = response.transaction_hash
            tx_hash = '0x0' + hex(decimal_value)[2:]
            tx_res = await self.starknet_client.account.client.wait_for_tx(
                response.transaction_hash
            )
            tx_status = tx_res.finality_status.value
            return f'{self.starknet_client.hex_address} | 10kSwap | swap {amount_in.Ether} ETH to {token_name} ' \
                   f' | tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}'

        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'

    async def swap_token_to_eth(self, token_name: str):
        """ Swap USDC/DAI/USDT/WBTC to ETH """

        token_name = token_name.upper()
        failed_text = f'Failed swap {token_name} to ETH via 10kswap'
        try:
            token_address = Swap10K.CONTRACT_MAP[token_name]['token_address']

            amount_in = await self.starknet_client.get_balance(token_address=token_address)

            amount_out = await Base.get_amount_out(
                amount_in=amount_in,
                token_in_name=token_name,
                token_out_name='ETH'
            )

            token_contract = Contract(
                address=token_address,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account,
            )
            swap10k_contract = await Contract.from_address(
                address=models.SWAP10K_ROUTER,
                provider=self.starknet_client.account,
            )

            approve_call = token_contract.functions["approve"].prepare_call(
                spender=models.SWAP10K_ROUTER,
                amount=amount_in.Wei
            )
            swap_call = swap10k_contract.functions["swapExactTokensForTokens"].prepare_call(
                amountIn=amount_in.Wei,
                amountOutMin=amount_out.Wei,
                path=[
                    token_address,
                    models.ETH_ADDRESS
                ],
                to=self.starknet_client.account.address,
                deadline=int(time.time() + 20 * 60)
            )

            response = await self.starknet_client.account.execute_v1(
                calls=[approve_call, swap_call],
                auto_estimate=True
            )
            decimal_value = response.transaction_hash
            tx_hash = '0x0' + hex(decimal_value)[2:]
            tx_res = await self.starknet_client.account.client.wait_for_tx(
                response.transaction_hash
            )
            tx_status = tx_res.finality_status.value
            return f'{self.starknet_client.hex_address} | 10kSwap | swap {amount_in.Ether} ETH to {token_name} ' \
                   f' | tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}'
        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'
