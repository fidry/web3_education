# 4) Напишите запрос, который выведет среднее количество обменов (number_of_swaps),
# среднее количество сминченных NFT (number_of_nft_mints) и среднее количество лендингов (number_of_lending),
# сгруппированных по значениям столбца completed.

import asyncio

from sqlalchemy import select, func

from models import Wallet
from db_api import Session


async def main():
    async with Session() as session:
        stmt = select(
            Wallet.completed,
            func.avg(Wallet.number_of_swaps).label('avg_number_of_swaps'),
            func.avg(Wallet.number_of_nft_mints).label('number_of_nft_mints'),
            func.avg(Wallet.number_of_lending).label('number_of_lending'),
        ).group_by(
            Wallet.completed
        )

        res = await session.execute(stmt)
        print(res.all())


if __name__ == '__main__':
    asyncio.run(main())
