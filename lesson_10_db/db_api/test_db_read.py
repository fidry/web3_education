from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc, asc

from db_api.models import Wallet
from db_api.db_init import engine


with Session(engine) as session:
    # ----------------------- получение объектов -----------------------
    # обращения к базе не происходит (ленивая сессия)
    # stmt = select(Wallet).where(Wallet.number_of_swaps < 2000)

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
    # ).order_by(
    #     desc(Wallet.number_of_swaps)
    # )

    # print(session.scalars(stmt).all())
    # print(session.scalars(stmt).first())
    # print(session.scalars(stmt).fetchmany(3))
    # print(len(session.scalars(stmt).all()))

    # for wallet in session.scalars(stmt):
    #     print(wallet, wallet.number_of_swaps)

    # ----------------------- получение объектов (2 способ) -----------------------
    # criterion = (Wallet.number_of_swaps < 6) & (Wallet.number_of_lending < 4)
    # criterion = (Wallet.number_of_swaps < 1) | (Wallet.number_of_lending < 4)
    # wallets = session.query(Wallet).filter(criterion).all()
    # for wallet in wallets:
    #     print(wallet)

    # ----------------------- изменение объектов -----------------------
    # print('session.dirty:', session.dirty)
    #
    # wallet = session.scalars(stmt).first()
    # print('address:', wallet.address)
    # wallet.address = '000000000'
    #
    # print(session.dirty)
    #
    # # если хотим, чтобы изменения сохранились, не забываем коммитить сессию
    # session.commit()
