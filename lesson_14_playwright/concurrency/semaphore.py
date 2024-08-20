import asyncio
from asyncio import Semaphore
from aiohttp import ClientSession


async def get_url(url: str, session: ClientSession, semaphore: Semaphore):
    print('Waiting to acquire semaphore...')
    async with semaphore:
        print('Semaphore acquired, requesting...')
        response = await session.get(url)
        print(f'Finishing requesting: {await response.json()}')
        await asyncio.sleep(5)
        return response.status


async def get_url_legacy(url: str, session: ClientSession, semaphore: Semaphore):
    print('Waiting to acquire semaphore...')
    await semaphore.acquire()
    print('Semaphore acquired, requesting...')
    response = await session.get(url)
    print(f'Finishing requesting: {await response.json()}')
    await asyncio.sleep(5)
    semaphore.release()
    return response.status


async def main():
    semaphore: Semaphore = Semaphore(10)
    # Хотя мы запускаем 1000 задач, "одновременно" будут выполняться только 10 задач.
    async with ClientSession() as session:
        tasks = [
            asyncio.create_task(
                get_url_legacy(
                    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                    session,
                    semaphore
                )
            )
            for _ in range(1000)
        ]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
