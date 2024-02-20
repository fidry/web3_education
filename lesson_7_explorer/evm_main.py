import asyncio

from eth_async.client import Client
from eth_async.models import Networks


async def main():
    client = Client(network=Networks.Ethereum)

    address = '0x36F302d18DcedE1AB1174f47726E62212d1CcEAD'

    # print(
    #     await client.network.api.functions.account.balance(address=address)
    # )

    # res = (await client.network.api.functions.account.txlist(
    #     address=address,
    # ))['result']
    # for r in res:
    #     print(r)

    res = await client.transactions.find_txs(
        contract='0x32400084C286CF3E17e7B677ea9583e60a000324',
        function_name='requestL2Transaction',
        address=address,
    )
    for tx_hash, data in res.items():
        print(tx_hash, data)


asyncio.run(main())
