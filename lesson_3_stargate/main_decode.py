import asyncio

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount

from tasks.stargate import Stargate
from data.config import PRIVATE_KEY


async def main():
    client = Client(private_key=PRIVATE_KEY, network=Networks.Avalanche)
    client.transactions


if __name__ == '__main__':
    asyncio.run(main())
