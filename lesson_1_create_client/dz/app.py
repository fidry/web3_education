import asyncio

from eth_async.models import Networks
from eth_async.client import Client


async def check_wallet():
    while True:
        client = Client(network=Networks.Ethereum)
        balance = await client.wallet.balance()
        print(f'{client.account.address} | {client.account.key.hex()} | {balance.Ether}')

        if balance.Wei != 0:
            with open('succsess_wallets.txt', 'a') as f:
                f.write(f'{client.account.address} | {client.account.key.hex()} | {balance.Ether}')


async def main(count):
    tasks = []
    for i in range(count):
        tasks.append(asyncio.create_task(check_wallet()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main(10))
