# 5) Создайте функцию для удаления записей в таблице Wallet, где значение столбца completed равно True.

import asyncio

from sqlalchemy import select

from models import Wallet
from db_api import Session


async def remove_completed_wallets():
    async with Session() as session:
        stmt = select(Wallet).where(Wallet.completed.is_(True))
        for wallet in await session.scalars(stmt):
            await session.delete(wallet)


async def main():
    await remove_completed_wallets()


if __name__ == '__main__':
    asyncio.run(main())
