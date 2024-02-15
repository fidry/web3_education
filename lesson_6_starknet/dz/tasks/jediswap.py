'''
eth -> dai: https://starkscan.co/tx/0x03d0bb58ff39125aa423a94794fe5f26f45560b7c10e6dbbd64641c8951a8623
dai -> eth: https://starkscan.co/tx/0x04e98e379747d5897b9852ed8dccd54c764939bf13a8e3f917b78b482663dba8
'''

import time

from starknet_py.contract import Contract

from data import models
from data.models import TokenAmount, DEFAULT_TOKEN_ABI
from tasks.base import Base


class JediSwap(Base):
    NAME = 'JediSwap'
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
        failed_text = f'Failed swap ETH to {token_name} via jediswap'
        # try:
        eth_contract = Contract(
            address=models.ETH_ADDRESS,
            abi=DEFAULT_TOKEN_ABI,
            provider=self.starknet_client.account
        )

        token_address = JediSwap.CONTRACT_MAP[token_name]['token_address']
        token_decimal = await self.starknet_client.get_decimals(token_address)

        amount_out = await Base.get_amount_out(
            amount_in=amount_in,
            token_in_name='ETH',
            token_out_name=token_name,
            amount_out_decimals=token_decimal
        )

        jediswap_contact = await Contract.from_address(
            address=models.JEDISWAP_ROUTER,
            provider=self.starknet_client.account,
            proxy_config=True
        )

        approve_call = eth_contract.functions['approve'].prepare(
            spender=models.JEDISWAP_ROUTER,
            amount=amount_in.Wei
        )
        swap_args = {
            'path': [models.ETH_ADDRESS, token_address],
            'to': self.starknet_client.account.address,
            'deadline': int(time.time() + 20 * 60),
            'amountOut': amount_out.Wei,
            'amountInMax': amount_in.Wei,
        }

        swap_call = jediswap_contact.functions['swap_tokens_for_exact_tokens'].prepare(**swap_args)

        response = await self.starknet_client.account.execute(
            calls=[approve_call, swap_call],
            auto_estimate=True
        )

        decimal_value = response.transaction_hash
        tx_hash = '0x0' + hex(decimal_value)[2:]
        tx_res = await self.starknet_client.account.client.wait_for_tx(
            response.transaction_hash
        )
        tx_status = tx_res.finality_status.value
        return f'{self.starknet_client.hex_address} | jediswap | swap {amount_in.Ether} ETH to {token_name} ' \
               f' | tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}'
        # except Exception as err:
        #     return f'{failed_text}: something went wrong: {err}'

    async def swap_token_to_eth(self, token_name: str):
        """ Swap USDC/DAI/USDT/WBTC to ETH """

        token_name = token_name.upper()
        failed_text = f'Failed swap {token_name} to ETH via jediswap'
        try:
            token_address = JediSwap.CONTRACT_MAP[token_name]['token_address']

            amount_in = await self.starknet_client.get_balance(token_address=token_address)

            amount_out = await Base.get_amount_out(
                amount_in=amount_in,
                token_in_name=token_name,
                token_out_name='ETH'
            )

            token_contract = Contract(
                address=token_address,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account
            )
            jediswap_contact = await Contract.from_address(
                address=models.JEDISWAP_ROUTER,
                provider=self.starknet_client.account,
                proxy_config=True
            )

            approve_call = token_contract.functions['approve'].prepare(
                spender=models.JEDISWAP_ROUTER,
                amount=amount_in.Wei
            )

            swap_args = {
                'path': [token_address, models.ETH_ADDRESS],
                'to': self.starknet_client.account.address,
                'deadline': int(time.time() + 20 * 60),
                'amountIn': amount_in.Wei,
                'amountOutMin': amount_out.Wei
            }

            swap_call = jediswap_contact.functions['swap_exact_tokens_for_tokens'].prepare(**swap_args)

            response = await self.starknet_client.account.execute(
                calls=[approve_call, swap_call],
                auto_estimate=True
            )
            decimal_value = response.transaction_hash
            tx_hash = '0x0' + hex(decimal_value)[2:]
            tx_res = await self.starknet_client.account.client.wait_for_tx(
                response.transaction_hash
            )
            tx_status = tx_res.finality_status.value
            return f'{self.starknet_client.hex_address} | jediswap | swap {amount_in.Ether} {token_name} to ETH ' \
                   f' | tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}'
        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'
