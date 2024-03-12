from datetime import datetime

from sqlalchemy.orm import Session
from db_api.models import Wallet

from db_api.db_init import engine


# Создание объекта класса Wallet
wallet = Wallet(
    private_key='0x8732y87g23b23y322dsfs',
    address='11111',
    next_action_time=datetime.now(),
    number_of_swaps=5,
    number_of_nft_mints=1,
    number_of_lending=4,
    number_of_liquidity_stake=2,
)


print('address:', wallet.address)

# id недоступен так как объект еще в в БД
print('id:', wallet.id)


session = Session(bind=engine)


# возвращает список объектов, которые уйдут в БД при коммите
print('session.new:', session.new)

# добавление объекта в сессию
session.add(wallet)
print('session.new:', session.new)

# отправляем объект в базу
session.commit()


# id теперь появился
print('id:', wallet.id)


# добавление сразу нескольких объектов (списком)
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
session.add_all([wallet_2, wallet_3])
session.commit()
