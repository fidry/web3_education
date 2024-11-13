import asyncio

from loguru import logger
from playwright.async_api import BrowserContext

from data.models import Wallet


class Uniswap:
    def __init__(self, context: BrowserContext, wallet: Wallet):
        self.context = context
        self.wallet = wallet

    async def connect_wallet(self):
        uniswap_url = 'https://app.uniswap.org/'

        uniswap_page = await self.context.new_page()
        await uniswap_page.goto(uniswap_url)
        await uniswap_page.wait_for_load_state(state='networkidle')

        # connect wallet btn
        await uniswap_page.locator(
            '//*[@id="AppHeader"]/div[2]/nav/div/div[3]/div[2]/div/button'
        ).click()

        logger.info(self.context.pages)

        # mm btn
        await uniswap_page.locator(
            '//*[@id="wallet-dropdown-scroll-wrapper"]/div/div/div[5]/div[1]/div/div[1]/button'
        ).click()

        await asyncio.sleep(3)
        logger.info(self.context.pages)

        mm_page = self.context.pages[-1]

        # further
        await mm_page.locator(
            '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'
        ).click()

        # confirm
        await mm_page.locator(
            '//*[@id="app-content"]/div/div/div/div[3]/div[2]/footer/button[2]'
        ).click()
