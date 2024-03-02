import asyncio

from evm_explorers.explorer_api import APIFunctions
from evm_explorers import config


async def main():
    api = APIFunctions(key=config.ETHEREUM_API_KEY, url='https://api.etherscan.io/api')

    # print(
    #     int((await api.account.balance(address=''))['result']) / 10 ** 18
    # )

    # addresses = ['0x36F302d18DcedE1AB1174f47726E62212d1CcEAD', '']
    # print(
    #     await api.account.balancemulti(address=addresses)
    # )

    # print(
    #     await api.account.txlist(address='')
    # )
    # res = (await api.account.txlist(address=''))['result']
    # for r in res:
    #     print(r)

    # print(
    #     await api.contract.getabi(address='0x32400084C286CF3E17e7B677ea9583e60a000324')
    # )

    print(
        await api.transaction.getstatus(
            txhash='0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a')
    )


asyncio.run(main())
