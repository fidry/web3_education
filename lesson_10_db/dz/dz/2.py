# 2) Напишите функцию для получения всех записей в таблице Wallet, отсортированных
# по количеству совершенных обменов (number_of_swaps).

import asyncio

from sqlalchemy import select

from models import Wallet
from db_api import Session, AsyncSessionLocal


async def get_sorted_wallets(session: AsyncSessionLocal) -> list[Wallet]:
    stmt = select(Wallet).order_by(Wallet.number_of_swaps)
    wallets = await session.scalars(stmt)
    return list(wallets.all())


async def main():
    async with Session() as session:
        wallets = await get_sorted_wallets(session)
        for wallet in wallets:
            print(wallet, wallet.number_of_swaps)


if __name__ == '__main__':
    asyncio.run(main())
