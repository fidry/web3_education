import asyncio

from playwright.async_api import async_playwright
from loguru import logger

import utils
import settings
from metamask.restore_wallet import restore_wallet
from metamask.uniswap import Uniswap
from wallets import WALLETS


async def process_wallet(wallet):
    async with async_playwright() as p:
        if settings.PROXY:
            proxy = await utils.format_proxy(settings.PROXY)

        args: list = [
            f"--disable-extensions-except={settings.MM_EXTENTION_PATH}",
            f"--load-extension={settings.MM_EXTENTION_PATH}"
        ]
        if settings.HEADLESS:
            args.append(f"--headless=new")

        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=args,
            proxy=proxy,
            slow_mo=settings.SLOW_MO
        )
        if not await restore_wallet(context=context, wallet=wallet):
            logger.error(f'{wallet.address}: Can not restore wallet')
            return
        await asyncio.sleep(3)

        logger.success('Start trade')

        uniswap = Uniswap(context=context, wallet=wallet)
        await uniswap.connect_wallet()
        await asyncio.sleep(999)


async def main():
    await process_wallet(wallet=WALLETS[1])


if __name__ == '__main__':
    asyncio.run(main())
