import asyncio
from datetime import datetime

from sqlalchemy import select, and_, desc

from db_api_async.models import Wallet
from db_api_async.db_api import Session


async def main():
    async with Session() as session:
        # ----------------------- получение объектов -----------------------
        # обращения к базе не происходит (ленивая сессия)
        # stmt = select(Wallet).where(Wallet.number_of_swaps < 2)

        stmt = select(Wallet).where(Wallet.number_of_swaps < 10).where(Wallet.number_of_lending <= 4)

        # stmt = select(
        #     Wallet
        # ).where(
        #     and_(
        #         Wallet.number_of_swaps < 10,
        #         Wallet.number_of_lending <= 4
        #     )
        # ).where(
        #     Wallet.next_action_time < datetime.now()
        # ).order_by(desc(Wallet.number_of_swaps))

        # print(
        #     (await session.scalars(stmt)).all()
        # )
        # print(
        #     (await session.scalars(stmt)).first()
        #  )
        # print(
        #     (await session.scalars(stmt)).fetchmany(2)
        # )
        # print(
        #     len((await session.scalars(stmt)).all())
        # )

        # for wallet in await session.scalars(stmt):
        #     print(wallet, wallet.number_of_swaps)

        # ----------------------- изменение объектов -----------------------
        # print('session.dirty:', session.dirty)
        #
        # wallet = (await session.scalars(stmt)).first()
        # print('address:', wallet.address)
        # wallet.address = '000000000'
        #
        # print(session.dirty)


if __name__ == '__main__':
    asyncio.run(main())
