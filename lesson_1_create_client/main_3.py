import asyncio

from eth_async.client import Client
from eth_async.models import Networks

from data.config import pk, seed


async def main():
    client = Client(private_key=pk, network=Networks.Ethereum)
    contract = await client.contracts.default_token(contract_address='0xaf88d065e77c8cc2239327c5edb3a432268e5831')
    print(type(contract))
    print(await contract.functions.decimals().call())

    print((await client.wallet.balance()).Wei)
    print((await client.wallet.balance(token_address='0xaf88d065e77c8cc2239327c5edb3a432268e5831')).Ether)

    print('nonce:', await client.wallet.nonce())


if __name__ == '__main__':
    asyncio.run(main())
