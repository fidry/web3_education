import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount

from tasks.mute import Mute
from tasks.space_fi import SpaceFi
from tasks.base import Base
from data.config import PRIVATE_KEY
from data.models import Contracts


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.ZkSync)
    mute = Mute(client=client)
    space_fi = SpaceFi(client=client)
    base = Base(client=client)

    # print(mute.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(mute.swap_eth_to_wbtc(amount=TokenAmount(0.0001)))
    # print(mute.swap_usdc_to_eth())
    # print(mute.swap_wbtc_to_eth())

    # print(await space_fi.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_usdt(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_wbtc(amount=TokenAmount(0.001)))
    # print(await client.wallet.balance(token=Contracts.ceBUSD))
    
    # print(await mute.swap_wbtc_to_eth())
    # print(await space_fi.swap_usdc_to_eth())
    # print(await space_fi.swap_busd_to_eth())
    # print(await space_fi.swap_usdt_to_eth())


if __name__ == '__main__':
    asyncio.run(main())
