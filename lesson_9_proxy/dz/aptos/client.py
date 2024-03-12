import random
from typing import Union, Optional, Any
import requests
import time

from loguru import logger

from aptos_sdk import ed25519
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from aptos_sdk.client import RestClient, ResourceNotFound, ApiError
from aptos_sdk.account import Account
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    SignedTransaction,
    RawTransaction
)
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.data.models import TokenAmount, ResourceType, Tokens, Token, SwapRouters, SwapRouterInfo
from aptos.utils.utils import get_explorer_hash_link, prepare_address_for_aptoscan_api
from data.models import Tx
from aptos.utils.utils import async_get, async_post


class AptosClient(RestClient):
    node_url = 'https://fullnode.mainnet.aptoslabs.com/v1'

    def __init__(self, private_key: str, proxy: Optional[str] = None):
        super().__init__(AptosClient.node_url)
        self.private_key = private_key
        self.signer = Account.load_key(self.private_key)
        self.address = AccountAddress.from_key(ed25519.PrivateKey.from_hex(private_key).public_key()).hex()
        self.proxy = proxy

        if self.proxy and '://' not in self.proxy:
            self.proxy = 'http://' + self.proxy

        self.client_config.max_gas_amount = 100000

    def get_coin_data(self, token: Token) -> Optional[dict]:
        try:
            coin_store_address = f'{ResourceType.store}<{token.address}>'
            coin_data = self.account_resource(account_address=self.signer.address(), resource_type=coin_store_address)
            return coin_data
        except:
            try:
                self.register(token)
            except Exception as e:
                logger.error(f'Get coin data error: {str(e)}')
        return {}

    def get_decimals(self, token: Token) -> int:
        try:
            token_address = AccountAddress.from_hex(token.address.split('::')[0])
            coin_info = self.account_resource(
                account_address=token_address, resource_type=f'{ResourceType.info}<{token.address}>')
            return coin_info['data']['decimals']
        except Exception as e:
            # logger.error(f'Get coin info error: {str(e)}')
            return 0

    def get_balance(self, token: Optional[Token] = None) -> Optional[TokenAmount]:
        if not token:
            token = Tokens.APT
        coin_data = self.get_coin_data(token)
        balance = coin_data.get('data', {}).get('coin', {}).get('value')
        decimals = self.get_decimals(token=token)

        if balance is not None:
            return TokenAmount(amount=int(balance), decimals=decimals, wei=True)
        return TokenAmount(amount=0, decimals=decimals, wei=True)

    def get_sorted_token_balance_dict(
            self,
            exclude_tokens: Optional[list[Token]] = None,
            include_zero_balance_tokens: bool = False
    ) -> dict[Token, TokenAmount]:
        exclude_tokens_names = []
        if exclude_tokens:
            exclude_tokens_names = [token.name for token in exclude_tokens]

        token_balance_dict = {}
        tokens = self.get_account_tokens()

        allowed_tokens = []
        for tokens_lst in Tokens.TOKENS_LIST, Tokens.LP_TOKENS_LIST:
            for token_ in tokens_lst:
                allowed_tokens.append(token_.name)

        for token in tokens:
            if exclude_tokens_names and token.name in exclude_tokens_names:
                continue

            if token.name not in allowed_tokens:
                continue

            balance = self.get_balance(token=token)
            if not include_zero_balance_tokens and balance.Wei <= 0:
                continue
            token_balance_dict[token] = balance
        return dict(sorted(token_balance_dict.items(), key=lambda item: item[1].Ether, reverse=True))

    def get_token_with_max_balance(self) -> Optional[Token]:
        max_balance = TokenAmount(amount=0, decimals=8)
        res_token = Tokens.APT
        try:
            for token in Tokens.TOKENS_LIST:
                balance = self.get_balance(token=token)
                if token.name != Tokens.APT.name:
                    balance_in_apt = self.get_token_balance_in_apt(amount_in=balance, from_token=token)
                else:
                    balance_in_apt = balance
                if float(balance_in_apt.Ether) > float(max_balance.Ether):
                    max_balance = balance_in_apt
                    res_token = token
            return res_token
        except Exception as err:
            logger.error(f'Can not get max balance error: {str(err)}')
        return None

    def get_token_balance_in_apt(
            self,
            amount_in: TokenAmount,
            from_token: Token,
            to_token: Token = Tokens.APT
    ) -> TokenAmount:
        try:
            dex = SwapRouters.LiquidSwap
            resource_account = AccountAddress.from_hex(dex.resource_account)
            curve_uncorrelated = dex.curve_uncorrelated

            try:
                resource_type = f'{dex.resource_type}<{from_token.address}, {to_token.address}, {curve_uncorrelated}>'
                data = self.account_resource(resource_type=resource_type, account_address=resource_account)['data']
                coin_x_reserve_value = int(data['coin_x_reserve']['value'])
                coin_y_reserve_value = int(data['coin_y_reserve']['value'])
            except:
                resource_type = f'{dex.resource_type}<{to_token.address}, {from_token.address}, {curve_uncorrelated}>'
                data = self.account_resource(resource_type=resource_type, account_address=resource_account)['data']
                coin_y_reserve_value = int(data['coin_x_reserve']['value'])
                coin_x_reserve_value = int(data['coin_y_reserve']['value'])

            reserve_x = TokenAmount(amount=coin_x_reserve_value, decimals=self.get_decimals(from_token), wei=True)
            reserve_y = TokenAmount(amount=coin_y_reserve_value, decimals=self.get_decimals(to_token), wei=True)

            return TokenAmount(
                amount=float(amount_in.Ether) * float(reserve_y.Ether) / float(reserve_x.Ether),
                decimals=8
            )
        except IndexError as e:
            logger.error(
                f'Simulation tx to get token balance in apt error: {str(e)}')
        except Exception as e:
            logger.error(f'Can\'t get token balance in apt: {str(e)}')

    def get_wallet_balance_in_apt(self) -> TokenAmount:
        result = TokenAmount(amount=0, decimals=8)
        for token in Tokens.TOKENS_LIST:
            balance = self.get_balance(token=token)
            if token.name != Tokens.APT.name:
                balance = self.get_token_balance_in_apt(amount_in=balance, from_token=token)
            result = TokenAmount(
                amount=result.Wei + balance.Wei,
                decimals=balance.decimals,
                wei=True
            )
        return result

    def get_account_tokens(self, account_address: Optional[AccountAddress] = None):
        if not account_address:
            account_address = self.address

        url = f'https://fullnode.mainnet.aptoslabs.com/v1/accounts/{account_address}/resources?limit=9999'
        if self.proxy is None:
            response = self.client.get(url)
        else:
            response = requests.get(url, proxies={'https': self.proxy})
        tokens_list = []
        for resource in response.json():
            resource_type = str(resource['type'])
            if ResourceType.store in resource_type:
                address = resource_type.split('<')[1][:-1]
                name = address.split('::')[-1]
                tokens_list.append(Token(name=name, address=address))
        return tokens_list

    @staticmethod
    def get_type_args(dex: SwapRouterInfo, from_token: Token, to_token: Token) -> list[TypeTag]:
        try:
            type_args = [
                TypeTag(StructTag.from_str(from_token.address)),
                TypeTag(StructTag.from_str(to_token.address))
            ]
            if dex.name == "liquidswap":
                type_args.append(TypeTag(StructTag.from_str(dex.curve_uncorrelated)))
            return type_args
        except Exception as e:
            logger.error(f"Get type args error for {dex}: {str(e)}")

    def register(self, token: Token) -> None:
        try:
            payload = EntryFunction.natural(
                '0x1::managed_coin',
                'register',
                [TypeTag(StructTag.from_str(token.address))],
                [],
            )
            signed_transaction = self.create_bcs_signed_transaction(
                sender=self.signer, payload=TransactionPayload(payload)
            )
            tx = self.submit_bcs_transaction(signed_transaction)
            self.wait_for_transaction(tx)
            logger.success(f'Token \'{token}\' is registered: {get_explorer_hash_link(tx)}')
            time.sleep(random.randint(10, 30))
        except Exception as e:
            if 'account_not_found' in str(e):
                logger.error(f'{self.address} | Account wasn\'t activated, send gas to activate this account')
            else:
                logger.error(f'Register token error: {str(e)}')

    @staticmethod
    def get_tx_info(version: Union[str, int]) -> Tx:
        url = f'https://fullnode.mainnet.aptoslabs.com/v1/transactions/by_version/{version}'
        response = requests.get(url).json()
        return Tx(
            version=response.get('version'),
            tx_hash=response.get('hash'),
            success=response.get('success'),
            changes=response.get('changes'),
            sender=response.get('sender'),
            nonce=response.get('sequence_number'),
            max_gas_amount=response.get('max_gas_amount'),
            gas_unit_price=response.get('gas_unit_price'),
            payload=response.get('payload'),
            signature=response.get('signature'),
            events=response.get('events'),
            tx_type=response.get('type'),
        )

    def get_tx_list(self, timestamp_from: int = 0, timestamp_to: int = 0) -> list[Tx]:
        tx_list = []
        address = prepare_address_for_aptoscan_api(self.address)
        url = f'https://api.aptoscan.com/api?module=account&action=txlist&address={address}&sort=asc'
        response = requests.get(url).json()
        if response['status'] == '1' and response['message'] == 'OK':
            txs = response['result']

            for tx in txs:
                if tx.get('expirationTime') and (timestamp_from <= int(tx['expirationTime']) <= timestamp_to):
                    tx_list.append(AptosClient.get_tx_info(version=tx['version']))
        return tx_list

    # ------------------------------ функции из основной библиотеки с поддержкой прокси ------------------------------
    def account_resource(
            self,
            resource_type: str,
            account_address: Optional[AccountAddress] = None,
            ledger_version: int = None
    ) -> dict[str, Any]:
        if not account_address:
            account_address = self.address
        if not ledger_version:
            request = f'{self.base_url}/accounts/{account_address}/resource/{resource_type}'
        else:
            request = f'{self.base_url}/accounts/{account_address}/resource/{resource_type}' \
                      f'?ledger_version={ledger_version}'

        if self.proxy is None:
            response = self.client.get(request)
        else:
            response = requests.get(
                request, proxies={'https': self.proxy})

        if response.status_code == 404:
            raise ResourceNotFound(resource_type, resource_type)
        if response.status_code >= 400:
            raise ApiError(
                f'{response.text} - {account_address}', response.status_code)
        return response.json()

    async def account_resource_async(
            self,
            resource_type: str,
            account_address: Optional[AccountAddress] = None,
            ledger_version: int = None
    ) -> dict[str, Any]:
        if not account_address:
            account_address = self.address
        if not ledger_version:
            request = f'{self.base_url}/accounts/{account_address}/resource/{resource_type}'
        else:
            request = f'{self.base_url}/accounts/{account_address}/resource/{resource_type}' \
                      f'?ledger_version={ledger_version}'

        if self.proxy is None:
            status_code, response = await async_get(url=request)
        else:
            status_code, response = await async_get(url=request, proxy=self.proxy)

        if status_code == 404:
            raise ResourceNotFound(resource_type, resource_type)
        if status_code >= 400:
            raise ApiError(
                f'{response} - {account_address}', status_code)
        return response

    def submit_bcs_transaction(self, signed_transaction: SignedTransaction) -> str:
        headers = {"Content-Type": "application/x.aptos.signed_transaction+bcs"}

        if self.proxy is None:
            response = self.client.post(
                f"{self.base_url}/transactions",
                headers=headers,
                data=signed_transaction.bytes(),
            )
        else:
            response = requests.post(
                f"{self.base_url}/transactions",
                headers=headers,
                data=signed_transaction.bytes(),
                proxies={"https": self.proxy}
            )

        if response.status_code >= 400:
            raise ApiError(response.text, response.status_code)
        return response.json()["hash"]

    async def submit_bcs_transaction_async(self, signed_transaction: SignedTransaction) -> str:
        headers = {"Content-Type": "application/x.aptos.signed_transaction+bcs"}

        if self.proxy is None:
            status_code, response = await async_post(
                url=f"{self.base_url}/transactions",
                headers=headers,
                data=signed_transaction.bytes(),
            )
        else:
            status_code, response = await async_post(
                url=f"{self.base_url}/transactions",
                headers=headers,
                data=signed_transaction.bytes(),
                proxy=self.proxy
            )

        if status_code >= 400:
            raise ApiError(response, status_code)
        return response["hash"]

    def wait_for_transaction(self, txn_hash: str) -> None:
        count = 0
        while self.transaction_pending(txn_hash):
            assert (
                    count < self.client_config.transaction_wait_in_seconds
            ), f"transaction {txn_hash} timed out"
            time.sleep(1)
            count += 1

        if self.proxy is None:
            response = self.client.get(
                f"{self.base_url}/transactions/by_hash/{txn_hash}")
        else:
            response = requests.get(
                f"{self.base_url}/transactions/by_hash/{txn_hash}",
                proxies={"https": self.proxy}
            )
        assert (
                "success" in response.json() and response.json()["success"]
        ), f"{response.text} - {txn_hash}"

    async def wait_for_transaction_async(self, txn_hash: str) -> None:
        count = 0
        while await self.transaction_pending_async(txn_hash):
            assert (
                    count < self.client_config.transaction_wait_in_seconds
            ), f"transaction {txn_hash} timed out"
            time.sleep(1)
            count += 1

        if self.proxy is None:
            status_code, response = await async_get(
                url=f"{self.base_url}/transactions/by_hash/{txn_hash}",
            )
        else:
            status_code, response = await async_get(
                url=f"{self.base_url}/transactions/by_hash/{txn_hash}",
                proxy=self.proxy
            )
        assert (
                "success" in response and response["success"]
        ), f"{response} - {txn_hash}"

    def transaction_pending(self, txn_hash: str) -> bool:
        if self.proxy is None:
            response = self.client.get(
                f"{self.base_url}/transactions/by_hash/{txn_hash}")
        else:
            response = requests.get(
                f"{self.base_url}/transactions/by_hash/{txn_hash}",
                proxies={"https": self.proxy}
            )
        if response.status_code == 404:
            return True
        if response.status_code >= 400:
            raise ApiError(response.text, response.status_code)
        return response.json()["type"] == "pending_transaction"

    async def transaction_pending_async(self, txn_hash: str) -> bool:
        if self.proxy is None:
            status_code, response = async_get(url=f"{self.base_url}/transactions/by_hash/{txn_hash}")
        else:
            status_code, response = async_get(
                url=f"{self.base_url}/transactions/by_hash/{txn_hash}",
                proxy=self.proxy
            )
        if status_code == 404:
            return True
        if status_code >= 400:
            raise ApiError(response, status_code)
        return response["type"] == "pending_transaction"

    def simulate_transaction(self, transaction: RawTransaction, sender: Account) -> dict[str, Any]:
        authenticator = Authenticator(Ed25519Authenticator(
            sender.public_key(), ed25519.Signature(b"\x00" * 64)))
        signed_transaction = SignedTransaction(transaction, authenticator)

        headers = {"Content-Type": "application/x.aptos.signed_transaction+bcs"}
        if self.proxy is None:
            response = self.client.post(
                f"{self.base_url}/transactions/simulate",
                headers=headers,
                data=signed_transaction.bytes()
            )
        else:
            response = requests.post(
                f"{self.base_url}/transactions/simulate",
                headers=headers,
                data=signed_transaction.bytes(),
                proxies={"https": self.proxy}
            )
        if response.status_code >= 400:
            raise ApiError(response.text, response.status_code)

        return response.json()
