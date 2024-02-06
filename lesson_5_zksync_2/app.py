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
from data.config import PRIVATE_KEY
from data.models import Contracts


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.ZkSync)
    mute = Mute(client=client)
    space_fi = SpaceFi(client=client)
    sync_swap = SyncSwap(client=client)
    maverick = Maverick(client=client)
    base = Base(client=client)

    # input_data = '0xc04b8d59000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000b7a4557a2bbd392a89fbe80aa726cbd645d112cb0000000000000000000000000000000000000000000000000000000065c0eac900000000000000000000000000000000000000000000000000038d7ea4c680000000000000000000000000000000000000000000000000000000000000231af3000000000000000000000000000000000000000000000000000000000000003c5aea5775959fbc2557cc8789bc1bf90a239d9a9141c8cf74c27554a8972d3bf3d2bd4a14d8b604ab3355df6d4c9c3035724fd0e3914de96a5a83aaf400000000,0x12210e8a'
    # base.parse_params(input_data)

    '''
    0xc04b8d59
    00  0000000000000000000000000000000000000000000000000000000000000020 - link
    20  00000000000000000000000000000000000000000000000000000000000000a0 - len
    40  000000000000000000000000b7a4557a2bbd392a89fbe80aa726cbd645d112cb - address
    60  0000000000000000000000000000000000000000000000000000000065c0eac9 - deadline
    80  00000000000000000000000000000000000000000000000000038d7ea4c68000 - amountIn
    a0  0000000000000000000000000000000000000000000000000000000000231af3 - amountOut
    c0  000000000000000000000000000000000000000000000000000000000000003c - len
    e0  5aea5775959fbc2557cc8789bc1bf90a239d9a9141c8cf74c27554a8972d3bf3 - path
    100 d2bd4a14d8b604ab3355df6d4c9c3035724fd0e3914de96a5a83aaf400000000 - path

    5aea5775959fbc2557cc8789bc1bf90a239d9a91 - WETH
    41c8cf74c27554a8972d3bf3d2bd4a14d8b604ab - WETH/USDC pool
    3355df6d4c9c3035724fd0e3914de96a5a83aaf4 - USDC
    00000000
    
    ,0x12210e8a
    '''

    # await base.get_token_info(contract_address='0x41c8cf74c27554a8972d3bf3d2bd4a14d8b604ab')

    # print(mute.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(mute.swap_eth_to_wbtc(amount=TokenAmount(0.0001)))
    # print(mute.swap_usdc_to_eth())
    # print(mute.swap_wbtc_to_eth())

    # print(await space_fi.swap_eth_to_usdc(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_usdt(amount=TokenAmount(0.0001)))
    # print(await space_fi.swap_eth_to_wbtc(amount=TokenAmount(0.001)))
    # print(await client.wallet.balance(token=Contracts.ceBUSD))
    #
    # print(await mute.swap_wbtc_to_eth())
    # print(await space_fi.swap_usdc_to_eth())
    # print(await space_fi.swap_busd_to_eth())
    # print(await space_fi.swap_usdt_to_eth())

    # print(
    #     await sync_swap.swap_eth_to_usdc(amount=TokenAmount(0.0001))
    # )

    print(
        await maverick.swap_eth_to_usdc(amount=TokenAmount(0.0001))
    )


if __name__ == '__main__':
    asyncio.run(main())
