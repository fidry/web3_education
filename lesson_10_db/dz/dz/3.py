# 3) Реализуйте функцию, которая обновляет next_action_time для указанной записи Wallet.

import asyncio
from datetime import datetime

from sqlalchemy import select

from models import Wallet
from db_api import Session


async def update_next_action_time(private_key: str, next_action_time: datetime):
    async with Session() as session:
        stmt = select(Wallet).where(Wallet.private_key == private_key)
        wallet = (await session.scalars(stmt)).first()
        if wallet:
            wallet.next_action_time = next_action_time


async def main():
    await update_next_action_time(private_key='0x8732y87g23b23y322dsfs', next_action_time=datetime.now())


if __name__ == '__main__':
    asyncio.run(main())
