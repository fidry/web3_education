# 7) Напишите функцию для поиска кошельков (Wallet),
# у которых значение в столбце address содержит определенную строку.
# Например, функция должна находить все кошельки, адреса которых содержат подстроку "abc".

import asyncio

from sqlalchemy import select

from models import Wallet
from db_api import Session


async def get_wallets_by_address(address: str):
    async with Session() as session:
        stmt = select(Wallet).where(
            Wallet.address.contains(address)
        )
        for wallet in await session.scalars(stmt):
            print(wallet.address)


async def main():
    await get_wallets_by_address(
        address='1'
    )


if __name__ == '__main__':
    asyncio.run(main())
