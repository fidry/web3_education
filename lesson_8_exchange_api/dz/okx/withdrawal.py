import random
import asyncio

from loguru import logger
from web3 import AsyncWeb3
from eth_typing import ChecksumAddress

from py_okx_async.models import Chains
from okx.okx_actions import OKXActions
from data import config


def randfloat(from_: float, to_: float, decimal_places: int = 0) -> float:
    # real, fraction = str(random.uniform(from_, to_)).split('.')
    # if decimal_places:
    #     fraction = fraction[:decimal_places]
    # return float('.'.join(
    #     [real, fraction]
    # ))

    return int((random.uniform(from_, to_) * 10 ** decimal_places)) / 10 ** decimal_places


def get_rows(path: str) -> list[str]:
    wallet_addresses = []
    with open(path) as f:
        for wallet_address in f:
            wallet_addresses.append(wallet_address.strip())
    return wallet_addresses


def add_row_to_file(path: str, row: str):
    with open(path, 'a') as f:
        f.write(row.strip() + '\n')


async def check_wallet_balance_evm(rpc: str, wallet_address: str | ChecksumAddress, token_address: str | None = None):
    wallet_address = AsyncWeb3.to_checksum_address(wallet_address)
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))

    if not token_address:
        coin_decimal = 18
        balance_wei = await w3.eth.get_balance(wallet_address)
        balance_eth = balance_wei / 10 ** coin_decimal
        return balance_eth
    else:
        token_address = AsyncWeb3.to_checksum_address(token_address)

        token_abi = [
            {
                'constant': True,
                'inputs': [],
                'name': 'decimals',
                'outputs': [{'name': '', 'type': 'uint256'}],
                'payable': False,
                'stateMutability': 'view',
                'type': 'function'
            },
            {
                'constant': True,
                'inputs': [{'name': 'who', 'type': 'address'}],
                'name': 'balanceOf',
                'outputs': [{'name': '', 'type': 'uint256'}],
                'payable': False,
                'stateMutability': 'view',
                'type': 'function'
            },
        ]
        contract = w3.eth.contract(address=token_address, abi=token_abi)
        balance_wei = await contract.functions.balanceOf(wallet_address).call()
        decimals = await contract.functions.decimals(wallet_address).call()
        balance_eth = balance_wei / 18 ** decimals
        return balance_eth


async def check_gas_price(max_gas_price_gwei: float, rpc: str, sleep: int = 60):
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    gas_price = await w3.eth.gas_price
    gas_price_gwei = AsyncWeb3.from_wei(gas_price, unit='gwei')

    while gas_price_gwei > max_gas_price_gwei:
        logger.info(f'Current gas price is too high: {gas_price_gwei} > {gas_price_gwei}!')
        await asyncio.sleep(sleep)
        gas_price = await w3.eth.gas_price
        gas_price_gwei = AsyncWeb3.from_wei(gas_price, unit='gwei')


async def okx_withdraw_evm(
        chain: str,
        token_symbol: str,
        wallet_address: str | ChecksumAddress,
        rpc: str,
        amount_to_withdraw: float | None = None,
        sleep: int = 60
) -> bool:
    try:
        okx = OKXActions(credentials=config.okx_credentials)

        # await check_gas_price(
        #     max_gas_price_gwei=config.maximum_gas_price,
        #     rpc=rpc,
        #     sleep=sleep
        # )

        if not amount_to_withdraw:
            amount_to_withdraw = randfloat(
                from_=config.withdraw_amount['from'],
                to_=config.withdraw_amount['to'],
                decimal_places=8
            )

        logger.info(f'{wallet_address}: start withdraw {amount_to_withdraw} {token_symbol} to {chain}')

        res = await okx.withdraw(
            to_address=wallet_address,
            amount=amount_to_withdraw,
            token_symbol=token_symbol,
            chain=chain
        )

        if not res:
            logger.error(f'{wallet_address}: can not get result of withdraw')
            return False

        if 'Failed' not in res:
            logger.success(f'{wallet_address} withdraw {amount_to_withdraw} {token_symbol} to {chain}: {res}')
            return True

        else:
            logger.error(f'{wallet_address} failed withdraw to {chain}: {res}')
        return False
    except Exception as err:
        logger.error(f'{wallet_address}: something went wrong: {err}')


async def main():
    wallets = set(get_rows(path=config.ADDRESSES_PATH))
    success_wallets = set(get_rows(path=config.SUCCESS_ADDRESSES_PATH))
    # failed_wallets = set(get_rows(path=config.FAILED_ADDRESSES_PATH))

    wallets = wallets - success_wallets

    for num, wallet_address in enumerate(wallets, start=1):
        logger.info(f'({num}/{len(wallets)}) {wallet_address}')
        res = await okx_withdraw_evm(
            chain=Chains.ArbitrumOne,
            token_symbol='ETH',
            wallet_address=wallet_address,
            rpc='https://1rpc.io/arb',
        )
        if res:
            add_row_to_file(path=config.SUCCESS_ADDRESSES_PATH, row=wallet_address)
            await asyncio.sleep(random.randint(
                config.delay_between_withdrawals['from'], config.delay_between_withdrawals['to']
            ))
        else:
            add_row_to_file(path=config.FAILED_ADDRESSES_PATH, row=wallet_address)

    logger.success(f'OKX withdraw successfully completed')


if __name__ == '__main__':
    asyncio.run(main())
