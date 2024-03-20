from __future__ import annotations
from typing import TYPE_CHECKING

from web3 import Web3
from eth_typing import ChecksumAddress
from web3.contract import AsyncContract, Contract

from .data.models import DefaultABIs, RawContract
from .utils.web_requests import async_get
from .utils.strings import text_between
from .data import types

if TYPE_CHECKING:
    from .client import Client


class Contracts:
    def __init__(self, client: Client) -> None:
        self.client = client

    async def default_token(self, contract_address: ChecksumAddress | str) -> Contract | AsyncContract:
        """
        Get a token contract instance with a standard set of functions.

        :param ChecksumAddress | str contract_address: the contract address or instance of token.
        :return Contract | AsyncContract: the token contract instance.
        """
        contract_address = Web3.to_checksum_address(contract_address)
        return self.client.w3.eth.contract(address=contract_address, abi=DefaultABIs.Token)

    @staticmethod
    async def get_signature(hex_signature: str) -> list | None:
        """
        Find all matching signatures in the database of https://www.4byte.directory/.

        :param str hex_signature: a signature hash.
        :return list | None: matches found.
        """
        try:
            response = await async_get(f'https://www.4byte.directory/api/v1/signatures/?hex_signature={hex_signature}')
            results = response['results']
            return [m['text_signature'] for m in sorted(results, key=lambda result: result['created_at'])]

        except:
            return

    @staticmethod
    async def parse_function(text_signature: str) -> dict:
        """
        Construct a function dictionary for the Application Binary Interface (ABI) based on the provided text signature.

        :param str text_signature: a text signature, e.g. approve(address,uint256).
        :return dict: the function dictionary for the ABI.
        """

        # swap(address,address,uint256,uint256,address,address)

        name, sign = text_signature.split('(', 1)
        sign = sign[:-1]
        tuples = []
        while '(' in sign:
            tuple_ = text_between(text=sign[:-1], begin='(', end=')')
            tuples.append(tuple_.split(',') or [])
            sign = sign.replace(f'({tuple_})', 'tuple')

        inputs = sign.split(',')
        if inputs == ['']:
            inputs = []

        function = {
            'type': 'function',
            'name': name,
            'inputs': [],
            'outputs': [{'type': 'uint256'}]
        }
        i = 0
        for type_ in inputs:
            input_ = {'type': type_}
            if type_ == 'tuple':
                input_['components'] = [{'type': comp_type} for comp_type in tuples[i]]
                i += 1

            function['inputs'].append(input_)

        return function

    @staticmethod
    async def get_contract_attributes(contract: types.Contract) -> tuple[ChecksumAddress, list | None]:
        """
        Convert different types of contract to its address and ABI.

        :param Contract contract: the contract address or instance.
        :return tuple[ChecksumAddress, list | None]: the checksummed contract address and ABI.
        """
        if isinstance(contract, (AsyncContract, RawContract)):
            return contract.address, contract.abi

        return Web3.to_checksum_address(contract), None

    async def get(
            self, contract_address: types.Contract, abi: list | str | None = None
    ) -> AsyncContract | Contract:
        """
        Get a contract instance.

        :param Contract contract_address: the contract address or instance.
        :param list | str | None abi: the contract ABI. (get it using the 'get_abi' function)
        :return AsyncContract: the contract instance.
        """
        contract_address, contract_abi = await self.get_contract_attributes(contract_address)
        if not abi and not contract_abi:
            # todo: в дальнейшем сделаем автоматическую загрузку abi из експлорера (в том числе через proxy_address)
            raise ValueError('Can not get abi for contract')

        if not abi:
            abi = contract_abi

        if abi:
            return self.client.w3.eth.contract(address=contract_address, abi=abi)

        return self.client.w3.eth.contract(address=contract_address)
