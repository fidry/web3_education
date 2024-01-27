'''
транза 1: https://arbiscan.io/tx/0xb12db5af2d2b04a0b413328b476b3192bf2bf20d2ffe586d5d99610f192298f4
транза 2: https://arbiscan.io/tx/0xb8b8c37baa32357f126284001e5e9f2e60767d2e8e7e5712a84a5eb0866cee03
'''

import json
import time

import requests
from fake_useragent import UserAgent
from web3.types import TxParams

from data.models import Contracts
from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount, Networks


class Uniswap(Base):
    @staticmethod
    async def get_price(amount: TokenAmount, slippage: float = 1.) -> TokenAmount:
        headers = {
            'authority': 'interface.gateway.uniswap.org',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.uniswap.org',
            'referer': 'https://app.uniswap.org/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent().chrome,
        }

        data = {
            "tokenInChainId": 42161,
            "tokenIn": "ETH",
            "tokenOutChainId": 42161,
            "tokenOut": str(Contracts.ARBITRUM_GETH.address),
            "amount": str(amount.Wei),
            "type": "EXACT_OUTPUT",
            "configs": [
                {
                    "protocols": [
                        "V2", "V3", "MIXED"
                    ],
                    "routingType": "CLASSIC"
                }
            ]
        }

        response = requests.post('https://api.uniswap.org/v2/quote', headers=headers, data=json.dumps(data))
        response_json = response.json()

        quote = int(response_json['quote']['quote'])
        slippage = slippage * -1
        amount_with_slippage = int(quote * (100 - slippage) / 100)
        return TokenAmount(
            amount=amount_with_slippage,
            decimals=18,
            wei=True
        )

    async def swap_eth_to_geth(
            self,
            amount_geth: TokenAmount,
            slippage: float = 1
    ) -> str:
        failed_text = f'Failed to buy GETH via Uniswap'

        if self.client.network.name != Networks.Arbitrum.name:
            return f'{failed_text}: wrong network ({self.client.network.name})'

        amount_eth = await Uniswap.get_price(amount=amount_geth, slippage=slippage)

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_UNISWAP_ROUTER)
        # todo: можно добавить проверку баланса

        args = TxArgs(
            commands='0x0b010c',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount_eth.Wei)[2:].zfill(64)}',

                f'0x{"1".zfill(64)}'
                f'{hex(amount_geth.Wei)[2:].zfill(64)}'
                f'{hex(amount_eth.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'dd69db25f6d620a7bad3023c5d32761d353d3de900271082af49447d8a07e3bd'
                f'95bd0d56f35241523fbab1000000000000000000000000000000000000000000',

                f'0x{"1".zfill(64)}{"".zfill(64)}',
            ],
            deadline=int(time.time() + 60 * 5)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount_eth.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount_eth.Ether} ETH was swapped to {amount_geth.Ether} GETH: {tx.hash.hex()}'

        return f'{failed_text}!'
