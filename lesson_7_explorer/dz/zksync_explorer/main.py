import asyncio

from zksync_explorer.explorer_api import get_txs_explorer, APIFunctions
from zksync_explorer import config


async def main():
    # print(
    #     await get_txs_explorer(
    #         account_address='0x32400084C286CF3E17e7B677ea9583e60a000324'
    #     )
    # )
    # res = (await get_txs_explorer(
    #     account_address='0x32400084C286CF3E17e7B677ea9583e60a000324',
    #     page_size=100
    # ))['items']
    # for r in res:
    #     print(r)
    # print(len(res))

    api_oklink = APIFunctions(url='https://www.oklink.com', key=config.OKLINK_API_KEY)
    # res = await api_oklink.account.txlist(
    #     address='0x32400084C286CF3E17e7B677ea9583e60a000324'
    # )
    # print(res)
    # print(len(res))

    res = await api_oklink.account.txlist_all(
        address='0x32400084C286CF3E17e7B677ea9583e60a000324'
    )
    print(res)
    print(len(res))


asyncio.run(main())
