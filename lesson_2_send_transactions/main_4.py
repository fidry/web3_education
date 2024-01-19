import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount

from data.config import pk
from tasks.woofi import WooFi


async def main():
    client = Client(private_key=pk, network=Networks.Arbitrum)
    woofi = WooFi(client=client)

    # eth_amount = TokenAmount(amount=0.001)
    # res = await woofi.swap_eth_to_usdc(amount=eth_amount)
    # print(res)

    # usdc_amount = TokenAmount(amount=10, decimals=6)
    # res = await woofi.swap_usdc_to_eth(amount=usdc_amount)
    # print(res)


if __name__ == '__main__':
    asyncio.run(main())
