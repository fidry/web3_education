import asyncio

from eth_async.client import Client
from eth_async.models import Networks


async def main():
    client = Client(network=Networks.Ethereum)

    address = ''

    # print(
    #     await client.network.api.functions.account.balance(address=address)
    # )

    # res = (await client.network.api.functions.account.txlist(
    #     address=address,
    # ))['result']
    # for r in res:
    #     print(r)

    # res = await client.transactions.find_txs(
    #     contract='',
    #     function_name='requestL2Transaction',
    #     address=address,
    # )
    # for tx_hash, data in res.items():
    #     print(tx_hash, data)

    # res = await client.transactions.find_tx_by_method_id(
    #     address=address,
    #     to='',
    #     method_id='',
    # )
    # for tx_hash, data in res.items():
    #     print(tx_hash, data)


asyncio.run(main())
