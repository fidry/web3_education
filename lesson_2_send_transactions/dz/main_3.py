import asyncio
import aiohttp

from eth_async.client import Client
from eth_async.models import Networks, TxArgs, TokenAmount

from data.models import Contracts
from data.config import pk


async def get_token_price(from_token, to_token) -> float | None:
    from_token, to_token = from_token.upper(), to_token.upper()
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://api.binance.com/api/v3/ticker/price?symbol={from_token + to_token}') as r:
            result_dict = await r.json()
            if 'msg' in result_dict and 'Invalid symbol' in result_dict['msg']:
                async with session.get(
                        f'https://api.binance.com/api/v3/ticker/price?symbol={to_token + from_token}') as r:
                    result_dict = await r.json()
            return float(result_dict['price'])


async def get_min_to_amount(from_token: str, to_token: str, decimals: float = 0.5):
    token_price = await get_token_price(from_token=from_token, to_token=to_token)
    return token_price * (1 - decimals / 100)


async def main():
    client = Client(private_key=pk, network=Networks.Arbitrum)

    from_token = Contracts.ARBITRUM_ETH
    to_token = Contracts.ARBITRUM_USDC

    woofi_contract = await client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)

    from_amount = TokenAmount(amount=0.001)
    min_to_amount = TokenAmount(
        amount=float(from_amount.Ether) * await get_min_to_amount(from_token=from_token.title, to_token=to_token.title),
        decimals=6
    )

    tx_args = TxArgs(
        fromToken=Contracts.ARBITRUM_ETH.address,
        toToken=Contracts.ARBITRUM_USDC.address,
        fromAmount=from_amount.Wei,
        minToAmount=min_to_amount.Wei,
        to=client.account.address,
        rebateTo=client.account.address,
    )

    tx_params = {
        'to': Contracts.ARBITRUM_WOOFI.address,
        'data': woofi_contract.encodeABI('swap', args=tx_args.tuple()),
        'value': from_amount.Wei
    }

    tx = await client.transactions.sign_and_send(tx_params=tx_params)
    receipt = await tx.wait_for_receipt(client=client, timeout=300)
    if receipt:
        print(f'Success: {tx.hash.hex()}')
    else:
        print(f'Error: {receipt} {tx.hash.hex()}')


if __name__ == '__main__':
    asyncio.run(main())
