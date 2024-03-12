import asyncio

from sqlalchemy import select

from db_api_async.models import Wallet
from db_api_async.db_api import Session


async def main():
    async with Session() as session:
        # получили нужные нам объекты и достали только первый из них
        stmp = select(Wallet).where(Wallet.address == '3333333')
        wallet = (await session.scalars(stmp)).first()
        print('address:', wallet.address)
        # удаляем этот объект
        await session.delete(wallet)


if __name__ == '__main__':
    asyncio.run(main())
