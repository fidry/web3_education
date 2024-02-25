import asyncio

from starknet_explorer.explorer_api import APIFunctions


async def main():
    api = APIFunctions(url='https://api.viewblock.io/starknet')

    # res = await api.account.txlist(
    #     # address='0x0128492ab86d97475cdc074a06a827014e6aa10da9bd745b26ccafb8c1a54a9a',
    #     address='0x0048d3bd46a594502de48b9508f457dea731768c56f3f77fc608b2498d9f872e',
    # )
    # print(res)

    res = await api.account.txlist_all(
        address='0x0128492ab86d97475cdc074a06a827014e6aa10da9bd745b26ccafb8c1a54a9a',
    )
    print(res)
    print(len(res))


asyncio.run(main())
