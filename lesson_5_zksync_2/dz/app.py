import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount
from web3 import Web3
from web3.types import HexStr

from tasks.mute import Mute
from tasks.space_fi import SpaceFi
from tasks.syncswap import SyncSwap
from tasks.base import Base
from tasks.maverick import Maverick
from tasks.official_bridge import OfficialBridge
from data.config import PRIVATE_KEY
from data.models import Contracts


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.ZkSync)
    mute = Mute(client=client)
    space_fi = SpaceFi(client=client)
    sync_swap = SyncSwap(client=client)
    maverick = Maverick(client=client)
    official_bridge = OfficialBridge(client=client)
    base = Base(client=client)

    # print(mute.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(mute.swap_eth_to_wbtc(amount=TokenAmount(0.0001)))
    # print(mute.swap_usdc_to_eth())
    # print(mute.swap_wbtc_to_eth())

    # print(await space_fi.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_usdt(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_wbtc(amount=TokenAmount(0.001)))
    # print(await client.wallet.balance(token=Contracts.ceBUSD))

    # print(await sync_swap.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(await sync_swap.swap_eth_to_usdt(amount=TokenAmount(0.0001)))
    # print(await sync_swap.swap_eth_to_busd(amount=TokenAmount(0.0001)))
    # print(await sync_swap.swap_eth_to_wbtc(amount=TokenAmount(0.0001)))

    # print(await sync_swap.swap_usdc_to_eth())
    # print(await sync_swap.swap_usdt_to_eth())
    # print(await sync_swap.swap_busd_to_eth())
    # print(await sync_swap.swap_wbtc_to_eth())

    # print(await official_bridge.deposit(amount=TokenAmount(0.01)))
    print(await official_bridge.withdraw(amount=TokenAmount(0.00001)))


if __name__ == '__main__':
    asyncio.run(main())
