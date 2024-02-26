import asyncio

from zksync_explorer.explorer_api import get_txs_explorer, APIFunctions
from zksync_explorer import config


async def main():
    # print(
    #     await get_txs_explorer(
    #         account_address=''
    #     )
    # )
    # res = (await get_txs_explorer(
    #     account_address='',
    #     page_size=100
    # ))['items']
    # for r in res:
    #     print(r)
    # print(len(res))

    api_oklink = APIFunctions(url='https://www.oklink.com', key=config.OKLINK_API_KEY)
    # res = await api_oklink.account.txlist(
    #     address=''
    # )
    # print(res)
    # print(len(res))

    # res = await api_oklink.account.txlist_all(address='')

    res = await api_oklink.account.find_tx_by_method_id(
        address='',
        to='',
        method_id=''
    )

    # for r in res:
    for r in res.items():
        print(r)
    print(len(res))


asyncio.run(main())
