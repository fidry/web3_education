import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount

from tasks.stargate import Stargate
from data.config import PRIVATE_KEY


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.Avalanche)
    stargate = Stargate(client=client)
    # res = await stargate.send_usdc(
    #     to_network=Networks.Avalanche,
    #     amount=TokenAmount(amount=2, decimals=6),
    # )

    res = await stargate.send_usdc_from_avalanche_to_usdt_bsc(
        amount=TokenAmount(amount=1, decimals=6),
        dest_fee=TokenAmount(amount=0.005),
    )

    print(res)


if __name__ == '__main__':
    asyncio.run(main())
