import asyncio

from loguru import logger
from playwright.async_api import BrowserContext, expect

from data.models import Wallet
import settings


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

    async def swap_eth_to_usdc(self):
        uniswap = self.context.pages[-1]

        # choose first token btn
        await uniswap.locator(
            '//*[@id="root"]/span/span/span/div/div[2]/div[10]/div/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div'
        ).click()

        # choose first token
        await uniswap.get_by_text(text='ZKsync ETH').click()

        # choose second token btn
        await uniswap.locator(
            '//*[@id="root"]/span/span/span/div/div[2]/div[10]/div/div/div/div[2]/div[1]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div'
        ).click()

        # choose second token
        await uniswap.get_by_test_id('token-option-324-USDC').click()

        # enter amount
        await uniswap.get_by_test_id('amount-input-in').fill(str(settings.ETH_TO_SELL))

        # review
        review_btn = uniswap.locator('//*[@id="root"]/span/span/span/div/div[2]/div[10]/div/div/div/div[2]/div[1]/div/div[2]/div/div[4]/div/div[1]/div[1]/div/span[1]/div')
        await expect(review_btn).to_be_enabled()
        await review_btn.click()

        # swap
        await asyncio.sleep(5)
        # full xpath
        swap_btn = uniswap.locator('//html/body/div[4]/span/span/div/div[2]/div/div/div[2]/div/span/div')
        await expect(swap_btn).to_be_enabled()
        await swap_btn.click()

        await asyncio.sleep(3)
        mm_page = self.context.pages[-1]

        # approve change network
        await mm_page.locator('//*[@id="app-content"]/div/div/div/div[2]/div[3]/button[2]').click()

        # change network
        await mm_page.locator('//*[@id="app-content"]/div/div/div/div[2]/div/button[2]').click()

        # try again btn
        try:
            try_again_btn = uniswap.locator(
                '//html/body/div[4]/span/span/div/div[2]/div/div/div/div/div[2]/div/div[2]/span/button')
            text = await try_again_btn.inner_text()
            if 'try again' in text.lower():
                await try_again_btn.click()
        except Exception as err:
            logger.error(err)

        await asyncio.sleep(2)
        mm_page = self.context.pages[-1]
        await mm_page.get_by_test_id('confirm-footer-button').click()

        logger.success('Success!!')
