# 6) Напишите функцию, которая будет выполнять запрос к базе данных и выводить список
# кошельков (Wallet), у которых next_action_time находится в определенном временном диапазоне,
# например, за последние 7 дней.

import asyncio
from datetime import datetime

from sqlalchemy import select, and_

from models import Wallet
from db_api import Session


async def get_wallets_by_date(from_: datetime, to_: datetime | None = None):
    if not to_:
        to_ = datetime.now()

    async with Session() as session:
        stmt = select(Wallet).where(
            and_(
                Wallet.next_action_time >= from_,
                Wallet.next_action_time <= to_,
            )
        )

        for wallet in await session.scalars(stmt):
            print(wallet.address, wallet.next_action_time)


async def main():
    now = datetime.now()

    await get_wallets_by_date(
        from_=datetime(year=now.year, month=now.month, day=5, hour=12, minute=12),
        to_=datetime(year=now.year, month=now.month, day=6, hour=22, minute=22)
    )


if __name__ == '__main__':
    asyncio.run(main())
