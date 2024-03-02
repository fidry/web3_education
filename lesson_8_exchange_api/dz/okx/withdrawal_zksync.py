import random
import asyncio

from loguru import logger
from web3 import Web3

from py_okx_async.models import Chains

from okx.okx_actions import OKXActions
from eth_async.client import Client
from eth_async.models import Networks, Network
from data import config


def randfloat(from_: float, to_: float, decimal_places: int = 0) -> float:
    # real, fraction = str(random.uniform(from_, to_)).split('.')
    # if decimal_places:
    #     fraction = fraction[:decimal_places]
    # return float('.'.join(
    #     [real, fraction]
    # ))

    return int((random.uniform(from_, to_) * 10 ** decimal_places)) / 10 ** decimal_places


def get_wallet_addresses(path: str) -> list[str]:
    wallet_addresses = []
    with open(path) as f:
        for wallet_address in f:
            wallet_addresses.append(wallet_address.strip())
    return wallet_addresses


async def is_there_official_bridge_txs(address: str) -> bool:
    address = Web3.to_checksum_address(address)

    txs = await Client(network=Networks.Ethereum).transactions.find_txs(
        address=address,
        contract='0x32400084c286cf3e17e7b677ea9583e60a000324',  # адрес контракта официального моста
        function_name='requestL2Transaction'
    )
    return bool(len(txs))


async def check_gas_price(gas_price_gwei: float, network: Network = Networks.Ethereum, sleep: int = 60):
    gas_price = await Client(network=network).transactions.gas_price()

    while float(Web3.from_wei(gas_price.Wei, unit='gwei')) > gas_price_gwei:
        logger.info(f'Current gas price is too high: '
                    f'{float(Web3.from_wei(gas_price.Wei, unit="gwei"))} > {gas_price_gwei}!')
        await asyncio.sleep(sleep)
        gas_price = await Client(network=network).transactions.gas_price()


async def okx_withdraw(wallet_addresses: list[str]):
    okx = OKXActions(credentials=config.okx_credentials)

    for num, address in enumerate(wallet_addresses, start=1):

        await check_gas_price(gas_price_gwei=config.maximum_gas_price)

        official_bridge_is_done = await is_there_official_bridge_txs(address=address)

        chain = None
        res = None
        amount_to_withdraw = 0

        if config.use_official_bridge and not official_bridge_is_done:
            # вывод в эфир
            chain = Chains.ERC20

            amount_to_withdraw = randfloat(
                from_=config.withdraw_amount_to_eth['from'],
                to_=config.withdraw_amount_to_eth['to'],
                decimal_places=8
            )

            logger.info(f'{num}/{len(wallet_addresses)} {address}: start withdraw {amount_to_withdraw} ETH to {chain}')

            res = await okx.withdraw(
                to_address=address,
                amount=amount_to_withdraw,
                token_symbol='ETH',
                chain=chain
            )

        elif official_bridge_is_done or not config.use_official_bridge:
            # вывод в зксинк
            chain = Chains.Starknet

            amount_to_withdraw = randfloat(
                from_=config.withdraw_amount_to_zksync['from'],
                to_=config.withdraw_amount_to_zksync['to'],
                decimal_places=8
            )

            logger.info(f'{num}/{len(wallet_addresses)} {address}: start withdraw {amount_to_withdraw} ETH to {chain}')

            res = await okx.withdraw(
                to_address=address,
                amount=amount_to_withdraw,
                token_symbol='ETH',
                chain=chain
            )

        if not chain or not res:
            logger.error(f'something went wrong: official_bridge_is_done: {official_bridge_is_done} | '
                         f'use_official_bridge: {config.use_official_bridge} | '
                         f'res: {res} | '
                         f'address: {address}')
            continue

        if 'Failed' not in res:
            logger.success(f'{address} withdraw {amount_to_withdraw} ETH to {chain}: {res}')

            await asyncio.sleep(random.randint(
                config.delay_between_withdrawals['from'], config.delay_between_withdrawals['to']
            ))

        else:
            logger.error(f'{address} failed withdraw to {chain}: {res}')

    logger.success(f'OKX withdraw successfully completed with {len(wallet_addresses)} wallets')


async def main():
    wallets = get_wallet_addresses(path=config.ADDRESSES_PATH)
    await okx_withdraw(wallet_addresses=wallets)


if __name__ == '__main__':
    asyncio.run(main())
