from loguru import logger
from playwright.async_api import BrowserContext

from data.models import Wallet
import settings


async def restore_wallet(context: BrowserContext, wallet: Wallet) -> bool:
    for num in range(1, settings.ATTEMPTS_NUMBER_RESTORE + 1):
        try:
            logger.info(f'{wallet.address} | Starting recover wallet')
            page = context.pages[0]
            await page.goto(f'chrome-extension://{settings.MM_EXTENTION_IDENTIFIER}/home.html#onboarding/welcome')
            await page.bring_to_front()

            await page.wait_for_load_state()

            # Agree checkbox
            await page.locator(
                '//*[@id="onboarding__terms-checkbox"]'
            ).click()

            # import wallet btn
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button'
            ).click()

            # no, thanks
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[1]'
            ).click()

            # fill seed phrase
            for i, word in zip(range(12), settings.MM_SEED.split()):
                await page.locator(f'//*[@id="import-srp__srp-word-{i}"]').fill(word)

            # confirm secret phrase
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'
            ).click()

            # fill password
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'
            ).fill(settings.EXTENTION_PASSWORD)
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'
            ).fill(settings.EXTENTION_PASSWORD)

            # agree checkbox
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input'
            ).click()

            # import wallet btn
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'
            ).click()

            # got it
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
            ).click()

            # next
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
            ).click()

            # done
            await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
            ).click()

            logger.success(f'{wallet.address} | Wallet Ready To Work')
            # await page.close()
            return True

        except Exception as err:
            logger.error(f'{wallet.address} | Not Recovered ({err})')
            logger.info(f'Error when getting an account, trying again, attempt No.{num}')

    return False
