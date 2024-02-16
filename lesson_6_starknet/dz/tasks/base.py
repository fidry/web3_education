import aiohttp
import asyncio

from proxy_client import StarknetClient
from data.models import TokenAmount


class Base:
    def __init__(self, starknet_client: StarknetClient):
        self.starknet_client = starknet_client

    @staticmethod
    async def get_token_price(token_symbol='ETH', second_token: str = 'USDT') -> float | None:
        token_symbol, second_token = token_symbol.upper(), second_token.upper()

        if token_symbol.upper() in ('USD', 'USDC', 'USDT', 'DAI', 'CEBUSD', 'BUSD'):
            return 1
        if token_symbol == 'WETH':
            token_symbol = 'ETH'

        for _ in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f'https://api.binance.com/api/v3/depth?limit=1&symbol={token_symbol}{second_token}') as r:
                        if r.status != 200:
                            return None
                        result_dict = await r.json()
                        if 'asks' not in result_dict:
                            return None
                        return float(result_dict['asks'][0][0])
            except Exception as e:
                await asyncio.sleep(5)
        raise ValueError(f'Can not get {token_symbol + second_token} price from Binance')

    @staticmethod
    async def get_amount_out(
            amount_in: TokenAmount,
            slippage: float = 1.,
            token_in_name: str = 'ETH',
            token_out_name: str = 'USDT',
            amount_out_decimals: int = 18
    ) -> TokenAmount:
        token_in_name, token_out_name = token_in_name.upper(), token_out_name.upper()

        token_in_usd = await Base.get_token_price(token_symbol=token_in_name)
        token_out_usd = await Base.get_token_price(token_symbol=token_out_name)

        return TokenAmount(
            amount=token_in_usd / token_out_usd * float(amount_in.Ether) * (100 - slippage) / 100,
            decimals=amount_out_decimals
        )
