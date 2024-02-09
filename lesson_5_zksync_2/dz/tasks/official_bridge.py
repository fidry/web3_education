from web3 import Web3

from eth_async.client import Client
from eth_async.models import TxArgs, Networks, TokenAmount

from data.models import Contracts
from tasks.base import Base


class OfficialBridge(Base):
    async def deposit(self, amount: TokenAmount) -> str:
        failed_text = 'Failed to bridge ETH to zkSync Era via the official bridge'
        eth_client = Client(private_key=self.client.account.key, network=Networks.Ethereum)
        contract = await eth_client.contracts.get(contract_address=Contracts.ETH_OFFICIAL_BRIDGE)
        balance = await eth_client.wallet.balance()
        gas_price = await eth_client.transactions.gas_price()
        gas_limit = 134_886
        l2_gas_limit = 397_207

        transaction_fee = TokenAmount(
            amount=gas_price.Wei * gas_limit,
            wei=True
        )

        if amount.Wei >= balance.Wei:
            amount = TokenAmount(
                amount=balance.Wei - transaction_fee.Wei * 1.2,
                wei=True
            )

        if amount.Wei < 0:
            return f'{failed_text}: Too low ETH balance; ETH balance: {balance.Ether}; ' \
                   f'Transaction fee: {transaction_fee.Ether}'

        # https://docs.zksync.io/build/tutorials/how-to/send-transaction-l1-l2.html#step-by-step
        max_fee = TokenAmount(
            amount=int(await contract.functions.l2TransactionBaseCost(gas_price.Wei, l2_gas_limit, 800).call() * 1.05),
            wei=True
        )

        if balance.Wei < amount.Wei + transaction_fee.Wei + max_fee.Wei:
            return f'{failed_text}: insufficient balance'

        args = TxArgs(
            _contractL2=eth_client.account.address,
            _l2Value=amount.Wei,
            _calldata=eth_client.w3.to_bytes(text=''),
            _l2GasLimit=l2_gas_limit,
            _l2GasPerPubdataByteLimit=800,
            _factoryDeps=[],
            _refundRecipient=eth_client.account.address
        )

        max_priority_fee_per_gas = Web3.to_wei(1.5, 'gwei')

        tx_params = {
            'from': self.client.account.address,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'maxFeePerGas': await eth_client.transactions.get_base_fee() + max_priority_fee_per_gas,
            'to': contract.address,
            'data': contract.encodeABI('requestL2Transaction', args=args.tuple()),
            'value': amount.Wei + max_fee.Wei
        }

        tx = await eth_client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=eth_client, timeout=300)
        if receipt:
            return f'{amount.Ether} ETH was deposited to zkSync Era via the official bridge: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def withdraw(self, amount: TokenAmount) -> str:
        failed_text = 'Failed to bridge to Ethereum'

        if self.client.network.name != Networks.ZkSync.name:
            return f'{failed_text} | wrong network ({self.client.network.name})'

        contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_OFFICIAL_BRIDGE)
        args = TxArgs(
            _l1Receiver=self.client.account.address
        )
        tx_params = {
            'from': self.client.account.address,
            'maxPriorityFeePerGas': Web3.to_wei(0.25, 'gwei'),
            'maxFeePerGas': Web3.to_wei(0.25, 'gwei'),
            'to': contract.address,
            'data': contract.encodeABI('withdraw', args=args.tuple()),
            'value': amount.Wei
        }

        gas_limit = await self.client.transactions.estimate_gas(tx_params=tx_params)
        tx_params['gas'] = gas_limit.Wei

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'ETH was withdraw to Ethereum via the official bridge: {tx.hash.hex()}'

        return f'{failed_text}!'
