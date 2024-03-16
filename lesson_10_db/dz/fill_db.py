import asyncio
from datetime import datetime

from models import Wallet
from db_api import Session


async def main():
    now = datetime.now()

    wallet1 = Wallet(
        private_key='0x8732y87g23b23y322dsfs',
        address='11111',
        next_action_time=datetime.now(),
        number_of_swaps=5,
        number_of_nft_mints=1,
        number_of_lending=4,
        number_of_liquidity_stake=2,
    )
    wallet_2 = Wallet(
        private_key='0x8732y87g23b23y2222222',
        address='2222222',
        next_action_time=datetime.now(),
        number_of_swaps=1,
        number_of_nft_mints=2,
        number_of_lending=3,
        number_of_liquidity_stake=4,
    )
    wallet_3 = Wallet(
        private_key='0x8732y87g23b23y3333333',
        address='3333333',
        next_action_time=datetime.now(),
        number_of_swaps=6,
        number_of_nft_mints=7,
        number_of_lending=8,
        number_of_liquidity_stake=9,
    )
    wallet_4 = Wallet(
        private_key='0x8732y87g23b23ysdkjfnskdjgnksd',
        address='444444444',
        next_action_time=datetime(year=now.year, month=now.month, day=5, hour=12, minute=12),
        number_of_swaps=6,
        number_of_nft_mints=7,
        number_of_lending=8,
        number_of_liquidity_stake=9,
    )
    wallet_5 = Wallet(
        private_key='0x8732y87g23b23fskdbfsdfbsdu78sdf',
        address='55555555',
        next_action_time=datetime(year=now.year, month=now.month, day=6, hour=22, minute=22),
        number_of_swaps=6,
        number_of_nft_mints=7,
        number_of_lending=8,
        number_of_liquidity_stake=9,
    )
    wallet_6 = Wallet(
        private_key='0x8732y87g23b23fskdbfsdsds8998987s9d',
        address='6666666',
        next_action_time=datetime(year=now.year, month=now.month, day=7, hour=2, minute=32),
        number_of_swaps=6,
        number_of_nft_mints=7,
        number_of_lending=8,
        number_of_liquidity_stake=9,
    )

    wallets = [
        wallet1, wallet_2, wallet_3, wallet_4, wallet_5, wallet_6
    ]

    async with Session() as session:
        session.add_all(wallets)


if __name__ == '__main__':
    asyncio.run(main())
