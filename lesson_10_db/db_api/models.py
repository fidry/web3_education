from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, Text, Boolean


class Base(DeclarativeBase):
    pass


# class Wallet(Base):
#     __tablename__ = 'wallets'
#
#     id = Column(Integer, primary_key=True)
#     private_key = Column(Text, unique=True, nullable=False, index=True)
#     address = Column(Text, nullable=False)
#     next_action_time = Column(Integer)
#     number_of_swaps = Column(Integer)
#     number_of_nft_mints = Column(Integer)
#     number_of_lending = Column(Integer)
#     number_of_liquidity_stake = Column(Integer)
#     completed = Column(Boolean, default=False, server_default='0')


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column(unique=True, index=True)
    address: Mapped[str]
    next_action_time: Mapped[datetime | None]
    number_of_swaps: Mapped[int]
    number_of_nft_mints: Mapped[int]
    number_of_lending: Mapped[int]
    number_of_liquidity_stake: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False, server_default='0')

    # def __str__(self):
    #     return f'{self.address}'

    def __repr__(self):
        return f'{self.address}'
