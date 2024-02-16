'''
1) написать функции для свапа eth в USDC/DAI/USDT/WBTC и обратно через jediswap
2) написать функции для свапа eth в USDC/DAI/USDT/WBTC и обратно через swap10k
3) написать функции на добавление и удаление ликвидности через myswap для пар USDT/ETH, USDC/ETH, DAI/ETH
'''

import asyncio

from proxy_client import StarknetClient
from data import config
from data.models import TokenAmount
from tasks.myswap import MySwap
from tasks.jediswap import JediSwap
from tasks.swap10k import Swap10K
from tasks.myswap_liquidity import MySwapLiquidity

from data import models


async def main():
    async with StarknetClient(
        private_key=config.private_key,
        account_address=config.account_address,
        proxy=config.proxy
    ) as starknet_client:
        amount = TokenAmount(0.001)

        my_swap = MySwap(starknet_client=starknet_client)
        # print(await my_swap.swap_eth_to_token(amount_in=amount, token_out_name='DAI'))
        # await my_swap.swap_token_to_eth(token_out_name='DAI')

        jediswap = JediSwap(starknet_client=starknet_client)
        # print(await jediswap.swap_eth_to_token(amount_in=amount, token_name='DAI'))
        # print(await jediswap.swap_token_to_eth(token_name='DAI'))

        swap10k = Swap10K(starknet_client=starknet_client)
        # print(await swap10k.swap_eth_to_token(amount_in=amount, token_name='USDT'))
        # print(await swap10k.swap_token_to_eth(token_name='USDT'))

        myswap_liquidity = MySwapLiquidity(starknet_client=starknet_client)
        # print(await myswap_liquidity.add_liquidity(token_out_name='DAI'))
        # print(await myswap_liquidity.remove_liquidity(token_out_name='DAI'))

        print(
            await starknet_client.get_balance(token_address=models.DAI_ADDRESS)
        )


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
