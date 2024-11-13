import asyncio

from loguru import logger
from playwright.async_api import BrowserContext, expect

from data.models import Wallet
import settings


class PhoenixTrade:
    def __init__(self, context: BrowserContext, wallet: Wallet):
        self.context = context
        self.wallet = wallet

    async def get_backpack_page(self):
        titles = [await p.title() for p in self.context.pages]
        backpack_page_index = 0

        for title in titles:
            if 'Backpack' in title:
                page = self.context.pages[backpack_page_index]
                await page.reload()
                return page
            backpack_page_index += 1

        backpack_page = await self.context.new_page()
        await backpack_page.goto(f'chrome-extension://{settings.EXTENTION_IDENTIFIER}/options.html?onboarding=true')
        return backpack_page

    async def get_phoenix_page(self):
        titles = [await p.title() for p in self.context.pages]
        phoenix_page_index = 0

        for title in titles:
            if 'Phoenix' in title:
                page = self.context.pages[phoenix_page_index]
                await page.reload()
                return page
            phoenix_page_index += 1

        phoenix_page = await self.context.new_page()
        await phoenix_page.goto(settings.PHOENIX_URL)
        return phoenix_page

    async def connect_wallet(self, max_retries: int = 10) -> None:
        logger.debug(f'{self.wallet.address} | Wallet Connecting To Phoenix')

        # phoenix_page = await self.context.new_page()
        for attempt in range(1, max_retries + 1):
            try:
                # делаем задержку (иногда браузер закрывает страничку backpack)
                await asyncio.sleep(5)
                phoenix_page = await self.get_phoenix_page()
                await asyncio.sleep(2)
                backpack_page = await self.get_backpack_page()

                await phoenix_page.bring_to_front()

                connect_wallet_btn = phoenix_page.locator(
                    '//*[@id="root"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[7]/div/button')
                await expect(connect_wallet_btn.first).to_be_visible()
                await connect_wallet_btn.click()

                choose_backpack_wallet_btn = phoenix_page.locator(
                    '//*[@id="root"]/div[1]/div/div/div[1]'
                )
                await expect(choose_backpack_wallet_btn.first).to_be_visible()
                await choose_backpack_wallet_btn.click()

                try:
                    unlock_btn = backpack_page.locator(
                        '//*[@id="root"]/span[1]/span/div/div/div[2]/div[2]/div[1]/div/div[2]/form/button'
                    )
                    await expect(unlock_btn.first).to_be_visible()
                    text_content = await unlock_btn.text_content()
                    # может быть написано не на английском
                    if text_content == 'Unlock':
                        await self.unlock_wallet()
                except:
                    pass

                await backpack_page.bring_to_front()
                approve_btn = backpack_page.locator(
                    '//*[@id="options"]/div/div/span/span/div/div/div[2]/div[2]/div[2]/div'
                )
                await expect(approve_btn.first).to_be_visible()
                await approve_btn.click()

                logger.success(f'{self.wallet.address} | Wallet Connected To Phoenix')
                return

            except Exception as e:
                logger.error(f'{self.wallet.address} | Error occurred: {str(e)}')
                if attempt <= max_retries:
                    logger.info(f'Retrying... (Attempt {attempt} of {max_retries})')
                else:
                    logger.error(f'{self.wallet.address} | Unable to connect after {max_retries} attempts')
                    raise

    async def unlock_wallet(self) -> None:
        logger.debug(f'{self.wallet.address} | Starting to Unlock Wallet')
        backpack_page = await self.get_backpack_page()
        await backpack_page.bring_to_front()
        # nth() используется для выбора элемента с определённым индексом из множества элементов,
        # найденных по предыдущему селектору
        password_input = backpack_page.get_by_placeholder("Password").nth(1)
        await expect(password_input.first).to_be_visible()
        await password_input.type(settings.EXTENTION_PASSWORD)

        unlock_btn = backpack_page.get_by_text(text='Unlock').nth(1)
        await expect(unlock_btn.first).to_be_enabled()
        await unlock_btn.click()
        logger.debug(f'{self.wallet.address} | Wallet Unlocked')

    async def sell_sol(self, max_retries: int = 10) -> None:
        # todo: добавить возможность отправки транзакции fast
        logger.debug(f'{self.wallet.address} | Starting Swap SOL to USDT')
        backpack_page = await self.get_backpack_page()
        phoenix_page = await self.get_phoenix_page()
        for attempt in range(1, max_retries + 1):
            try:
                await phoenix_page.bring_to_front()

                sell_btn = phoenix_page.get_by_text(text='Sell')
                await expect(sell_btn.first).to_be_visible()
                await sell_btn.click()

                market_sell_btn = phoenix_page.get_by_text(text='Market')
                await expect(market_sell_btn.first).to_be_visible()
                await market_sell_btn.click()

                # количество соланы на кошельке можно взять из UI
                # inpot_amount
                await phoenix_page.locator(
                    '//*[@id="root"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/div/input'
                ).type(str(settings.SOL_TO_SELL))

                place_market_order_btn = phoenix_page.locator(
                    '//*[@id="root"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/div/button'
                )
                place_market_order_btn_text = await place_market_order_btn.text_content()

                if place_market_order_btn_text in [
                    'Enter an amount',
                    'Insufficient SOL balance',
                    'Insufficient size'
                ]:
                    await backpack_page.reload()
                    logger.warning(f'{self.wallet.address} | Place Order Button Not Working')
                    continue

                await expect(place_market_order_btn.first).to_be_enabled()
                await place_market_order_btn.click()
                try:
                    unlock_btn = backpack_page.locator(
                        '//*[@id="root"]/span[1]/span/div/div/div[2]/div[2]/div[1]/div/div[2]/form/button'
                    )
                    await expect(unlock_btn.first).to_be_visible()
                    text_content = await unlock_btn.text_content()
                    if text_content == 'Unlock':
                        await self.unlock_wallet()
                except:
                    pass

                await backpack_page.bring_to_front()
                await backpack_page.wait_for_load_state(state='networkidle')
                approve_btn = backpack_page.locator(
                    '//*[@id="options"]/div/div/span/span/div/div/div[3]/div[2]/div'
                )
                await expect(approve_btn.first).to_be_visible()
                await approve_btn.click()

                logger.success(f'{self.wallet.address} | Wallet Sell {round(settings.SOL_TO_SELL, 4)} SOL to USDT')

                await phoenix_page.bring_to_front()
                # todo: Проверить, табличку, что транзакция успешна
                return

            except Exception as e:
                logger.error(f'{self.wallet.address} | Error occurred: {str(e)}')
                await phoenix_page.reload()
                await backpack_page.reload()
                if attempt <= max_retries:
                    logger.info(f'Retrying... (Attempt {attempt} of {max_retries})')
                else:
                    logger.error(
                        f'{self.wallet.address} | Unable to complete SOL to USDT swap after {max_retries} attempts')
                    raise
