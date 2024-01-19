from __future__ import annotations
from typing import TYPE_CHECKING

from web3 import Web3
from eth_typing import ChecksumAddress
from web3.contract import AsyncContract, Contract

from .models import DefaultABIs

if TYPE_CHECKING:
    from .client import Client


class Contracts:
    def __init__(self, client: Client) -> None:
        self.client = client

    async def default_token(self, contract_address: ChecksumAddress | str) -> Contract | AsyncContract:
        contract_address = Web3.to_checksum_address(contract_address)
        return self.client.w3.eth.contract(address=contract_address, abi=DefaultABIs.Token)
