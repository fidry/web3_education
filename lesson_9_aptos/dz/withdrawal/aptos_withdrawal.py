import asyncio
import random

from py_okx_async.models import Chains
from loguru import logger

from db_api.models import Wallet
from withdrowal.okx_actions import OKXActions

from client import AptosClient
from utils.utils import randfloat
from data.models import Settings


async def okx_withdraw(wallets: list[Wallet]):
    settings = Settings()
    okx = OKXActions(credentials=settings.okx.credentials)
    for wallet in wallets:
        private_key = wallet.private_key
        aptos_client = AptosClient(private_key=private_key)
        balance = aptos_client.get_balance()

        if float(balance.Ether) >= 0.8:
            continue

        amount_to_withdraw = randfloat(
            from_=settings.okx.withdraw_amount.from_,
            to_=settings.okx.withdraw_amount.to_,
            step=0.0000001
        )
        amount_to_withdraw = amount_to_withdraw - float(balance.Ether)

        res = await okx.withdraw(
            to_address=aptos_client.address,
            amount=amount_to_withdraw,
            token_symbol='APT',
            chain='Starknet'
        )
        if 'Failed' not in res:
            logger.success(res)
            await asyncio.sleep(
                random.randint(settings.okx.delay_between_withdrawals.from_, settings.okx.delay_between_withdrawals.to_)
            )
        else:
            logger.error(res)
