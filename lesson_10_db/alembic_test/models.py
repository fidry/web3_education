from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    next_action_time: Mapped[datetime | None]
    number_of_swaps: Mapped[int]
    number_of_nft_mints: Mapped[int]
    number_of_lending: Mapped[int]
    number_of_liquidity_stake: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False)
    completed2: Mapped[bool] = mapped_column(default=False)
    completed3: Mapped[bool] = mapped_column(default=False, server_default='0')

    def __str__(self):
        return f'{self.address}'

    def __repr__(self):
        return f'{self.address}'
