import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount

from tasks.stargate import Stargate
from tasks.coredao import CoredaoBridge
from tasks.uniswap import Uniswap
from tasks.testnetbridge import Testnetbridge
from data.config import PRIVATE_KEY


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.Arbitrum)
    stargate = Stargate(client=client)
    coredao_bridge = CoredaoBridge(client=client)
    uniswap = Uniswap(client=client)
    testnetbridge = Testnetbridge(client=client)

    # res = await coredao_bridge.bridge_usdt_bsc_to_usdt_coredao(amount=TokenAmount(amount=0.01))
    # print(res)

    # res = await uniswap.swap_eth_to_geth(amount_geth=TokenAmount(0.1), slippage=10)
    # print(res)

    res = await testnetbridge.swap_geth(geth_amount=TokenAmount(0.01))
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
