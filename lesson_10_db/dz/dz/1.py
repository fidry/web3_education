# 1) Напишите функцию, которая добавляет новую запись в таблицу Wallet с указанными параметрами:
# private_key, address, next_action_time (остальные параметры генерируются рандомно).

import random
import asyncio
from datetime import datetime

from models import Wallet
from db_api import Session


async def add_new_wallet(private_key: str, address: str, next_action_time: datetime):
    wallet = Wallet(
        private_key=private_key,
        address=address,
        next_action_time=next_action_time,
        number_of_swaps=random.randint(1, 10),
        number_of_nft_mints=random.randint(1, 10),
        number_of_lending=random.randint(1, 10),
        number_of_liquidity_stake=random.randint(1, 10),
    )

    async with Session() as session:
        session.add(wallet)


async def main():
    await add_new_wallet(
        private_key='1111111',
        address='2222222',
        next_action_time=datetime.now()
    )

if __name__ == '__main__':
    asyncio.run(main())
