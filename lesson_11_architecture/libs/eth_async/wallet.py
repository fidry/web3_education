from __future__ import annotations
from typing import TYPE_CHECKING

from web3 import Web3
from eth_typing import ChecksumAddress
from web3.contract import AsyncContract

from .data.models import TokenAmount, RawContract
from .data import types

if TYPE_CHECKING:
    from .client import Client


class Wallet:
    def __init__(self, client: Client) -> None:
        self.client = client

    async def balance(
            self,
            token: types.Contract | None = None,
            address: str | ChecksumAddress | None = None,
            decimals: int = 18
    ) -> TokenAmount:
        if not address:
            address = self.client.account.address

        address = Web3.to_checksum_address(address)

        if not token:
            return TokenAmount(
                amount=await self.client.w3.eth.get_balance(account=address),
                decimals=decimals,
                wei=True
            )

        token_address = token
        if isinstance(token, (RawContract, AsyncContract)):
            token_address = token.address

        contract = await self.client.contracts.default_token(
            contract_address=Web3.to_checksum_address(token_address)
        )

        return TokenAmount(
            amount=await contract.functions.balanceOf(address).call(),
            decimals=await self.client.transactions.get_decimals(contract=contract.address),
            wei=True
        )

    async def nonce(self, address: ChecksumAddress | None = None) -> int:
        if not address:
            address = self.client.account.address
        return await self.client.w3.eth.get_transaction_count(address)
