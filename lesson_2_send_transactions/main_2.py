import asyncio

from eth_async.client import Client
from eth_async.models import Networks
from eth_async.utils.utils import read_json
from eth_async.transactions import Tx

from data.config import pk, ABIS_DIR
from data.models import Contracts


async def main():
    client = Client(private_key=pk, network=Networks.Arbitrum)

    print(
        await client.transactions.gas_price()
    )

    print(
        await client.transactions.max_priority_fee()
    )

    # tx_data = await client.w3.eth.get_transaction(transaction_hash='0x9e742b4c0d7d7c6059d708fbf6a8be683b51bddb8400a03a0dbe41b1387e8eb2')
    # print(tx_data)

    # tx = Tx(
    #     tx_hash='0x9e742b4c0d7d7c6059d708fbf6a8be683b51bddb8400a03a0dbe41b1387e8eb2',
    # )
    # print(await tx.parse_params(client=client))

    # print(
    #     await client.contracts.get_signature(hex_signature='0x7dc20382')
    # )

    # print(
    #     await client.contracts.parse_function(text_signature='swap(address,address,uint256,uint256,address,address)'),
    # )

    # print(
    #     await client.contracts.get_contract_attributes(contract=Contracts.WooFi)
    # )

    # contract = await client.contracts.get(
    #     contract_address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30',
    #     abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    # )

    # contract = await client.contracts.get(
    #     contract_address=Contracts.ARBITRUM_USDC,
    # )
    # print(await contract.functions.WETH().call())
    # print(await contract.functions.decimals().call())

    '''
    WooFi:
    0.001 ETH -> USDC   https://arbiscan.io//tx/0xdb91bbc608189bcedcd90facac0c1a2d48fec9ff624674ace728c7e488d6cc72
    
    Сайт для поиска по сигнатуре функции: https://www.4byte.directory/
    '''


if __name__ == '__main__':
    asyncio.run(main())
