import random

from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector

import starknet_py.cairo.felt
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner
from starknet_py.serialization import TupleDataclass

from data import config
from data.config import logger
from data.models import TokenAmount, DEFAULT_TOKEN_ABI


class StarknetClient:
    chain_id = StarknetChainId.MAINNET

    def __init__(self, private_key: int, account_address: int, proxy: str = ''):
        self.key_pair = KeyPair.from_private_key(private_key)
        self.signer = StarkCurveSigner(account_address, self.key_pair, StarknetClient.chain_id)

        self.hex_address = self.value_to_hex(account_address)
        self.proxy = StarknetClient.normalize_proxy(proxy=proxy)

        self.connector = None
        self.session = None
        self.starknet_client = None
        self.account = None

        if self.proxy:
            self.connector = ProxyConnector.from_url(self.proxy)
            self.session = ClientSession(connector=self.connector)
            self.starknet_client = FullNodeClient(
                node_url=random.choice(config.NODE_URLS),
                session=self.session
            )
        else:
            logger.warning(f'Proxy not used')
            # alchemy, blastapi
            self.starknet_client = FullNodeClient(node_url=random.choice(config.NODE_URLS))

        self.account = Account(
            address=account_address,
            client=self.starknet_client,
            key_pair=self.key_pair,
            chain=StarknetClient.chain_id
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.proxy:
            await self.session.close()

    async def get_decimals(self, token_address: int) -> int:
        contract = Contract(
            address=token_address,
            abi=DEFAULT_TOKEN_ABI,
            provider=self.account
        )
        return int(StarknetClient.get_data(
            await contract.functions['decimals'].call()
        ))

    async def get_balance(self, token_address: int) -> TokenAmount:
        return TokenAmount(
            amount=await self.account.get_balance(token_address=token_address, chain_id=StarknetClient.chain_id),
            decimals=await self.get_decimals(token_address=token_address),
            wei=True
        )

    def value_to_hex(self, value=None) -> str | None:
        if not value:
            return '0x{:064x}'.format(self.account.address)
        return '0x{:064x}'.format(value)

    @staticmethod
    def normalize_proxy(proxy: str = '') -> str:
        if proxy and 'http' not in proxy:
            proxy = f'http://{proxy}'
        return proxy

    @staticmethod
    def get_data(info: int | TupleDataclass | tuple | dict) -> int | float | str | bool:
        if isinstance(info, int) or isinstance(info, str):
            return info
        elif isinstance(info, TupleDataclass):
            return info.as_tuple()[0]
        elif isinstance(info, tuple):
            return info[0]
        elif isinstance(info, dict):
            return list(info.values())[0]
        return info

    @staticmethod
    def get_text_from_decimal(info: int | TupleDataclass | tuple | dict) -> str | None:
        info = StarknetClient.get_data(info)
        if isinstance(info, str) and info.isdigit():
            info = int(info)
        return str(starknet_py.cairo.felt.decode_shortstring(info)).replace('\0', '').strip()
