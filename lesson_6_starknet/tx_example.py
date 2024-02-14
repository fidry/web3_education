import asyncio

from tasks.myswap import MySwap
from proxy_client import StarknetClient
from data import config, models
from data.models import TokenAmount


async def main():
    async with StarknetClient(
            private_key=config.private_key,
            account_address=config.account_address,
            proxy=config.proxy
    ) as client:
        my_swap = MySwap(starknet_client=client)

        print(await client.get_balance(token_address=models.DAI_ADDRESS))

        # res = await my_swap.swap_eth_to_token(amount_in=TokenAmount(0.0001), token_out_name='DAI')
        # print(res)

        # res = await my_swap.swap_token_to_eth(token_in_name='DAI')
        # print(res)


if __name__ == '__main__':
    asyncio.run(main())

