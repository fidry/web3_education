import random
import time

from loguru import logger
from utils.db_api.models import Wallet
from withdrawal.okx_actions import OKXActions
from libs.py_okx_async.models import Chains
from libs.eth_async.client import Client
from libs.eth_async.data.models import Networks
from libs.eth_async.utils.utils import randfloat

from data.models import Settings


async def okx_withdraw(wallets: list[Wallet]):
    settings = Settings()
    okx = OKXActions(credentials=settings.okx.credentials)

    for num, wallet in enumerate(wallets, start=1):
        logger.info(f'{num}/{len(wallets)} wallets')

        eth_client = Client(private_key=wallet.private_key, network=Networks.Ethereum, proxy=wallet.proxy)
        zks_client = Client(private_key=wallet.private_key, network=Networks.ZkSync, proxy=wallet.proxy)

        if settings.use_official_bridge:
            balance = await eth_client.wallet.balance()
        else:
            balance = await zks_client.wallet.balance()

        if float(balance.Ether) >= settings.okx.required_minimum_balance:
            continue

        amount_to_withdraw = randfloat(
            from_=settings.okx.withdraw_amount.from_,
            to_=settings.okx.withdraw_amount.to_,
            step=0.0000001
        )

        res = await okx.withdraw(
            to_address=str(eth_client.account.address),
            amount=amount_to_withdraw,
            token_symbol='ETH',
            chain=Chains.ERC20 if settings.use_official_bridge else Chains.zkSyncEra
        )

        if 'Failed' not in res:
            logger.success(f'{wallet.name}: {res}')
            if num >= len(wallets):
                logger.success(f'OKX withdraw successfully completed with {len(wallets)} wallets')
                return

            time.sleep(random.randint(
                settings.okx.delay_between_withdrawals.from_, settings.okx.delay_between_withdrawals.to_))
        else:
            logger.error(f'{wallet.name}: {res}')
