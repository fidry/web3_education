'''
eth + usdt: https://starkscan.co/tx/0x0524c323058c5e4af88835a591268104816d52e93b40316c739b7f05fe412cba
withdraw: https://starkscan.co/tx/0x03b3c0398895e93e73f6befe1899e2bbcf9629f9a12527de5a7b090c8426044c
'''

from starknet_py.contract import Contract

from data import models
from tasks.base import Base
from data.models import DEFAULT_TOKEN_ABI

'''
AMM 

59977818973461968079 * 169405631502 = const

1000 USDT | 1 ETH
1000 * 1 = 1000 = const
A * B = const

Предположение: 0.1 ETH = 100$

1000 + 100 * X = const = 1000
1100 * X = 1000
X = 1000 / 1100 = 0.91 ETH

1 - 0.91 = 0.09
'''


class MySwapLiquidity(Base):
    NAME = 'MySwap'
    AVAILABLE_DEPOSIT = ['USDC', 'DAI', 'USDT']
    CONTRACT_MAP = {
        'USDC': {
            'token_address': models.USDC_ADDRESS,
            'liquidity_token_address': models.MYSWAP_ETH_USDC,
            'pool_name': 'ETH/USDC',
            'pool_id': 1,
        },
        'DAI': {
            'token_address': models.DAI_ADDRESS,
            'liquidity_token_address': models.MYSWAP_ETH_DAI,
            'pool_name': 'DAI/ETH',
            'pool_id': 2,
        },
        'USDT': {
            'token_address': models.USDT_ADDRESS,
            'liquidity_token_address': models.MYSWAP_ETH_USDT,
            'pool_name': 'ETH/USDT',
            'pool_id': 4,
        },
    }

    async def add_liquidity(self, token_out_name: str, slippage: float = 2.):
        """ add liquidity USDT/ETH, USDC/ETH, DAI/ETH """
        token_out_name = token_out_name.upper()
        pool_name = MySwapLiquidity.CONTRACT_MAP[token_out_name]['pool_name']
        token_address = MySwapLiquidity.CONTRACT_MAP[token_out_name]['token_address']

        failed_text = f'Failed add liquidity {pool_name} via myswap'
        try:
            token_amount = await self.starknet_client.get_balance(token_address=token_address)

            eth_amount = await Base.get_amount_out(
                amount_in=token_amount,
                token_in_name=token_out_name,
                token_out_name='ETH'
            )

            eth_contract = Contract(
                address=models.ETH_ADDRESS,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account
            )
            token_contract = Contract(
                address=token_address,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account
            )
            myswap_contract = await Contract.from_address(
                address=models.MY_SWAP_ROUTER,
                provider=self.starknet_client.account,
                proxy_config=True
            )

            token_approve_call = token_contract.functions['approve'].prepare_call(
                spender=models.MY_SWAP_ROUTER,
                amount=token_amount.Wei
            )
            eth_approve_call = eth_contract.functions['approve'].prepare_call(
                spender=models.MY_SWAP_ROUTER,
                amount=eth_amount.Wei
            )

            add_liquidity_call = myswap_contract.functions['add_liquidity'].prepare_call(
                a_address=token_address,
                a_amount=token_amount.Wei,
                a_min_amount=int(token_amount.Wei * (1 - slippage / 100)),
                b_address=models.ETH_ADDRESS,
                b_amount=eth_amount.Wei,
                b_min_amount=int(eth_amount.Wei * (1 - slippage / 100))
            )

            response = await self.starknet_client.account.execute_v1(
                calls=[token_approve_call, eth_approve_call, add_liquidity_call],
                auto_estimate=True
            )

            decimal_value = response.transaction_hash
            tx_hash = '0x0' + hex(decimal_value)[2:]
            tx_res = await self.starknet_client.account.client.wait_for_tx(
                response.transaction_hash
            )
            tx_status = tx_res.finality_status.value
            return f'{self.starknet_client.hex_address} | myswap | add liquidity {pool_name} | ' \
                   f'ETH: {eth_amount.Ether} + {token_out_name}: {token_amount.Ether} | tx: ' \
                   f' | tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}'

        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'

    async def remove_liquidity(self, token_out_name: str, slippage: float = 1):
        """ remove liquidity USDT/ETH, USDC/ETH, DAI/ETH """

        token_out_name = token_out_name.upper()
        pool_name = MySwapLiquidity.CONTRACT_MAP[token_out_name]['pool_name']
        lptoken_address = MySwapLiquidity.CONTRACT_MAP[token_out_name]['liquidity_token_address']
        pool_id = MySwapLiquidity.CONTRACT_MAP[token_out_name]['pool_id']

        failed_text = f'Failed remove liquidity {pool_name} via myswap'
        try:
            amount_in = await self.starknet_client.get_balance(lptoken_address)

            lptoken_contract = Contract(
                address=lptoken_address,
                abi=DEFAULT_TOKEN_ABI,
                provider=self.starknet_client.account
            )
            myswap_contract = await Contract.from_address(
                address=models.MY_SWAP_ROUTER,
                provider=self.starknet_client.account,
                proxy_config=True
            )

            # calculate min amount tokenA and tokenB
            total_pool_supply = await myswap_contract.functions['get_total_shares'].call(pool_id)
            total_pool_supply = total_pool_supply.total_shares

            amount_list = await myswap_contract.functions['get_pool'].call(pool_id)
            token_a_amount, token_b_amount = amount_list.pool['token_a_reserves'], amount_list.pool['token_b_reserves']

            amount_min_a = int(((amount_in.Wei / total_pool_supply) * token_a_amount) * (1 - slippage / 100))
            amount_min_b = int(((amount_in.Wei / total_pool_supply) * token_b_amount) * (1 - slippage / 100))

            approve_call = lptoken_contract.functions['approve'].prepare_call(
                spender=models.MY_SWAP_ROUTER,
                amount=amount_in.Wei
            )
            withdraw_liquidity_call = myswap_contract.functions['withdraw_liquidity'].prepare_call(
                pool_id=pool_id,
                shares_amount=amount_in.Wei,
                amount_min_a=amount_min_a,
                amount_min_b=amount_min_b
            )

            response = await self.starknet_client.account.execute_v1(
                calls=[approve_call, withdraw_liquidity_call],
                auto_estimate=True
            )

            decimal_value = response.transaction_hash
            tx_hash = '0x0' + hex(decimal_value)[2:]
            tx_res = await self.starknet_client.account.client.wait_for_tx(
                response.transaction_hash
            )
            tx_status = tx_res.finality_status.value
            return (f'{self.starknet_client.hex_address} | myswap | remove liquidity {pool_name} | '
                    f'tx_hash: https://starkscan.co/tx/{tx_hash} | status: {tx_status}')
        except Exception as err:
            return f'{failed_text}: something went wrong: {err}'
