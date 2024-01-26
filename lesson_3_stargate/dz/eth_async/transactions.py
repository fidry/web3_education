from __future__ import annotations
from typing import TYPE_CHECKING, Any
from hexbytes import HexBytes

from web3 import Web3, AsyncWeb3
from web3.types import TxReceipt, _Hash32, TxParams
from eth_account.datastructures import SignedTransaction

from .models import TokenAmount, CommonValues, TxArgs
from .classes import AutoRepr
from . import exceptions
from . import types

if TYPE_CHECKING:
    from .client import Client


class Tx(AutoRepr):
    """
    An instance of transaction for easy execution of actions on it.

    Attributes:
        hash (Optional[_Hash32]): a transaction hash.
        params (Optional[dict]): the transaction parameters.
        receipt (Optional[TxReceipt]): a transaction receipt.
        function_identifier (Optional[str]): a function identifier.
        input_data (Optional[Dict[str, Any]]): an input data.

    """
    hash: _Hash32 | None
    params: dict | None
    receipt: TxReceipt | None
    function_identifier: str | None
    input_data: dict[str, Any] | None

    def __init__(self, tx_hash: str | _Hash32 | None = None, params: dict | None = None) -> None:
        """
        Initialize the class.

        Args:
            tx_hash (Optional[Union[str, _Hash32]]): the transaction hash. (None)
            params (Optional[dict]): a dictionary with transaction parameters. (None)

        """
        if not tx_hash and not params:
            raise exceptions.TransactionException("Specify 'tx_hash' or 'params' argument values!")

        if isinstance(tx_hash, str):
            tx_hash = HexBytes(tx_hash)

        self.hash = tx_hash
        self.params = params
        self.receipt = None
        self.function_identifier = None
        self.input_data = None

    async def parse_params(self, client) -> dict[str, Any]:
        """
        Parse the parameters of a sent transaction.

        Args:
            client (Client): the Client instance.

        Returns:
            Dict[str, Any]: the parameters of a sent transaction.

        """
        tx_data = await client.w3.eth.get_transaction(transaction_hash=self.hash)
        self.params = {
            'chainId': client.network.chain_id,
            'nonce': int(tx_data.get('nonce')),
            'gasPrice': int(tx_data.get('gasPrice')),
            'gas': int(tx_data.get('gas')),
            'from': tx_data.get('from'),
            'to': tx_data.get('to'),
            'data': tx_data.get('input'),
            'value': int(tx_data.get('value'))
        }
        return self.params

    async def wait_for_receipt(
            self, client, timeout: int | float = 120, poll_latency: float = 0.1
    ) -> dict[str, Any]:
        """
        Wait for the transaction receipt.

        Args:
            client (Client): the Client instance.
            timeout (Union[int, float]): the receipt waiting timeout. (120 sec)
            poll_latency (float): the poll latency. (0.1 sec)

        Returns:
            Dict[str, Any]: the transaction receipt.

        """
        self.receipt = await client.transactions.wait_for_receipt(
            w3=client.w3,
            tx_hash=self.hash,
            timeout=timeout,
            poll_latency=poll_latency
        )
        return self.receipt

    async def decode_input_data(self):
        pass

    async def cancel(self):
        pass

    async def speed_up(self):
        pass


class Transactions:
    def __init__(self, client: Client) -> None:
        self.client = client

    async def gas_price(self) -> TokenAmount:
        """
        Get the current gas price
        :return: gas price
        """
        return TokenAmount(amount=await self.client.w3.eth.gas_price, wei=True)

    async def max_priority_fee(self) -> TokenAmount:
        """
        Get the current max priority fee.

        Returns:
            Wei: the current max priority fee.

        """
        return TokenAmount(amount=await self.client.w3.eth.max_priority_fee, wei=True)

    async def estimate_gas(self, tx_params: TxParams) -> TokenAmount:
        """
        Get the estimate gas limit for a transaction with specified parameters.

        Args:
            tx_params (TxParams): parameters of the transaction.

        Returns:
            Wei: the estimate gas.

        """
        return TokenAmount(
            amount=await self.client.w3.eth.estimate_gas(transaction=tx_params),
            wei=True,
        )

    async def auto_add_params(self, tx_params: TxParams) -> TxParams:
        """
        Add 'chainId', 'nonce', 'from', 'gasPrice' or 'maxFeePerGas' + 'maxPriorityFeePerGas' and 'gas' parameters to
            transaction parameters if they are missing.

        Args:
            tx_params (TxParams): parameters of the transaction.

        Returns:
            TxParams: parameters of the transaction with added values.

        """

        if 'chainId' not in tx_params:
            tx_params['chainId'] = self.client.network.chain_id

        if not tx_params.get('nonce'):
            tx_params['nonce'] = await self.client.wallet.nonce()

        if 'from' not in tx_params:
            tx_params['from'] = self.client.account.address

        if 'gasPrice' not in tx_params and 'maxFeePerGas' not in tx_params:
            gas_price = (await self.gas_price()).Wei
            if self.client.network.tx_type == 2:
                tx_params['maxFeePerGas'] = gas_price

            else:
                tx_params['gasPrice'] = gas_price

        elif 'gasPrice' in tx_params and not int(tx_params['gasPrice']):
            tx_params['gasPrice'] = (await self.gas_price()).Wei

        if 'maxFeePerGas' in tx_params and 'maxPriorityFeePerGas' not in tx_params:
            tx_params['maxPriorityFeePerGas'] = (await self.max_priority_fee()).Wei
            tx_params['maxFeePerGas'] = tx_params['maxFeePerGas'] + tx_params['maxPriorityFeePerGas']

        if 'gas' not in tx_params or not int(tx_params['gas']):
            tx_params['gas'] = (await self.estimate_gas(tx_params=tx_params)).Wei

        return tx_params

    async def sign_transaction(self, tx_params: TxParams) -> SignedTransaction:
        """
        Sign a transaction.

        Args:
            tx_params (TxParams): parameters of the transaction.

        Returns:
            SignedTransaction: the signed transaction.

        """
        return self.client.w3.eth.account.sign_transaction(
            transaction_dict=tx_params, private_key=self.client.account.key
        )

    async def sign_and_send(self, tx_params: TxParams) -> Tx:
        """
        Sign and send a transaction. Additionally, add 'chainId', 'nonce', 'from', 'gasPrice' or
            'maxFeePerGas' + 'maxPriorityFeePerGas' and 'gas' parameters to transaction parameters if they are missing.

        Args:
            tx_params (TxParams): parameters of the transaction.

        Returns:
            Tx: the instance of the sent transaction.

        """
        await self.auto_add_params(tx_params=tx_params)

        signed_tx = await self.sign_transaction(tx_params)

        tx_hash = await self.client.w3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)

        return Tx(tx_hash=tx_hash, params=tx_params)

    async def approved_amount(
            self, token: types.Contract, spender: types.Contract, owner: types.Address | None = None
    ) -> TokenAmount:
        """
        Get approved amount of token.

        Args:
            token (Contract): the contract address or instance of token.
            spender (Contract): the spender address, contract address or instance.
            owner (Optional[Address]): the owner address. (imported to client address)

        Returns:
            TokenAmount: the approved amount.

        """
        contract_address, abi = await self.client.contracts.get_contract_attributes(token)
        contract = await self.client.contracts.default_token(contract_address)
        spender, abi = await self.client.contracts.get_contract_attributes(spender)
        if not owner:
            owner = self.client.account.address

        return TokenAmount(
            amount=await contract.functions.allowance(
                Web3.to_checksum_address(owner),
                Web3.to_checksum_address(spender)
            ).call(),
            decimals=await self.client.transactions.get_decimals(contract=contract.address),
            wei=True
        )

    @staticmethod
    async def wait_for_receipt(
            w3: Web3 | AsyncWeb3, tx_hash: str | _Hash32, timeout: int | float = 120, poll_latency: float = 0.1
    ) -> dict[str, Any]:
        """
        Wait for a transaction receipt.

        Args:
            w3: web3 object
            tx_hash (Union[str, _Hash32]): the transaction hash.
            timeout (Union[int, float]): the receipt waiting timeout. (120)
            poll_latency (float): the poll latency. (0.1 sec)

        Returns:
            Dict[str, Any]: the transaction receipt.

        """
        return dict(await w3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=timeout, poll_latency=poll_latency
        ))

    async def approve(
            self, token: types.Contract, spender: types.Address, amount: types.Amount | None = None,
            gas_limit: types.GasLimit | None = None, nonce: int | None = None
    ) -> Tx:
        """
        Approve token spending for specified address.

        Args:
            token (Contract): the contract address or instance of token to approve.
            spender (Address): the spender address, contract address or instance.
            amount (Optional[TokenAmount]): an amount to approve. (infinity)
            gas_limit (Optional[GasLimit]): the gas limit in Wei. (parsed from the network)
            nonce (Optional[int]): a nonce of the sender address. (get it using the 'nonce' function)

        Returns:
            Tx: the instance of the sent transaction.

        """
        spender = Web3.to_checksum_address(spender)
        contract_address, abi = await self.client.contracts.get_contract_attributes(token)
        contract = await self.client.contracts.default_token(contract_address)

        if amount is None:
            amount = CommonValues.InfinityInt
        elif isinstance(amount, (int, float)):
            amount = TokenAmount(
                amount=amount,
                decimals=await self.client.transactions.get_decimals(contract=contract.address)
            ).Wei
        else:
            amount = amount.Wei

        tx_args = TxArgs(
            spender=spender,
            amount=amount
        )

        tx_params = {
            'nonce': nonce,
            'to': contract.address,
            'data': contract.encodeABI('approve', args=tx_args.tuple())
        }

        if gas_limit:
            if isinstance(gas_limit, int):
                gas_limit = TokenAmount(amount=gas_limit, wei=True)
            tx_params['gas'] = gas_limit.Wei

        return await self.sign_and_send(tx_params=tx_params)

    async def get_decimals(self, contract: types.Contract) -> int:
        contract_address, abi = await self.client.contracts.get_contract_attributes(contract)
        contract = await self.client.contracts.default_token(contract_address=contract_address)
        return await contract.functions.decimals().call()

    async def sign_message(self):
        pass

    @staticmethod
    async def decode_input_data():
        pass
