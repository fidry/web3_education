import asyncio

from eth_async.client import Client
from eth_async.models import Networks
from eth_async.transactions import Transactions

from data.config import pk, seed


async def main():
    client = Client(private_key=pk, network=Networks.Optimism)
    # contract = await client.contracts.default_token(contract_address='0xaf88d065e77c8cc2239327c5edb3a432268e5831')
    # print(type(contract))
    # print(await contract.functions.decimals().call())
    #
    # print((await client.wallet.balance()).Wei)
    # print((await client.wallet.balance(token_address='0xaf88d065e77c8cc2239327c5edb3a432268e5831')).Ether)
    #
    # print('nonce:', await client.wallet.nonce())

    gas_price = await client.transactions.gas_price()
    print(gas_price.Wei)


if __name__ == '__main__':
    asyncio.run(main())
