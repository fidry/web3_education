import random
from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import select, and_, or_

from data.models import Settings
from utils.db_api.wallet_api import db
from utils.db_api.models import Wallet


def update_expired(initial: bool = False) -> None:
    now = datetime.now()
    if initial:
        stmt = select(Wallet).where(
            and_(
                Wallet.initial_completed.is_(False),
                or_(
                    Wallet.next_initial_action_time <= now,
                    Wallet.next_initial_action_time.is_(None),
                )
            )
        )
    else:
        stmt = select(Wallet).where(
            and_(
                Wallet.initial_completed.is_(True),
                or_(
                    Wallet.next_activity_action_time <= now,
                    Wallet.next_activity_action_time.is_(None),
                )
            )
        )

    expired_wallets: list[Wallet] = db.all(stmt=stmt)

    if not expired_wallets:
        return

    settings = Settings()
    for wallet in expired_wallets:
        if initial:
            wallet.next_initial_action_time = now + timedelta(
                seconds=random.randint(0, int(settings.initial_actions_delay.to_ / 2))
            )
            logger.info(
                f'{wallet.address}: Action time was re-generated: '
                f'{wallet.next_initial_action_time}.'
            )
        else:
            wallet.next_activity_action_time = now + timedelta(
                seconds=random.randint(0, int(settings.activity_actions_delay.to_ / 3))
            )
            logger.info(
                f'{wallet.address}: Action time was re-generated: '
                f'{wallet.next_activity_action_time}.'
            )

    db.commit()
