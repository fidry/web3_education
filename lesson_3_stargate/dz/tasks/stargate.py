'''
Arbitrum:
arbitrum -> avalanche (2.5): https://arbiscan.io/tx/0x3ad0c8aa2b5675c3f6fbfde5fb6c668c95a99179db0b9f107a6068c7bfe0071b
arbitrum -> polygon (2.5): https://arbiscan.io/tx/0xad55c727e33ded6bfca74417705cebb31d307430b1da8dc8a17b02225e5a462a

Polygon:
polygon -> arbitrum (1): https://polygonscan.com/tx/0xc14084044d5abccb11647c9f6a6b2fa68df4551b828326d345bf27e77d755e38
polygon -> avalanche (1): https://polygonscan.com/tx/0x432b5592bb9bfdce14845844bd09c3bed9fc6bb54311608142ca60469e819346

Avalanche:
avalanche -> arbitrum (1): https://snowtrace.io/tx/0x0d14541440bf7731070649f9447365b61f7760b3f8895f8fa544265869a76e3c
avalanche -> polygon (1): https://snowtrace.io/tx/0x4716dcfa604b5e11cc8c930ecef8f7f0c42f05bd31d1eb1401c84fe798af9395
avalanche -> bsc (2.5 USDT): https://snowtrace.io/tx/0x47d2cfa1d89b1656c83c5548e0b5fd17cc54ea8f4674b3f02d0c324546778d53

Optimism:
optimism -> arbitrum (0.75): https://optimistic.etherscan.io/tx/0x7278b546cd4025d0f8e8120e77ff1a2d43344cf450bbe15e4114f9eb426d167f

'''

import asyncio
import random

from web3.types import TxParams
from web3.contract import AsyncContract
from eth_typing import ChecksumAddress

from eth_async.models import TxArgs, TokenAmount, Networks, Network
from eth_async.client import Client
from tasks.base import Base
from data.models import Contracts


class Stargate(Base):
    contract_data = {
        Networks.Arbitrum.name: {
            'usdc_contract': Contracts.ARBITRUM_USDC_e,
            'stargate_contract': Contracts.ARBITRUM_STARGATE,
            'stargate_chain_id': 110,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Avalanche.name: {
            'usdc_contract': Contracts.AVALANCHE_USDC,
            'stargate_contract': Contracts.AVALANCHE_STARGATE,
            'stargate_chain_id': 106,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Polygon.name: {
            'usdc_contract': Contracts.POLYGON_USDC,
            'stargate_contract': Contracts.POLYGON_STARGATE,
            'stargate_chain_id': 109,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Optimism.name: {
            'usdc_contract': Contracts.OPTIMISM_USDC,
            'stargate_contract': Contracts.OPTIMISM_STARGATE,
            'stargate_chain_id': 111,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.BSC.name: {
            'stargate_chain_id': 102,
            'src_pool_id': 1,
            'dst_pool_id': 2,
        }
    }

    async def send_usdc(
            self,
            to_network: Network,
            amount: TokenAmount | None = None,
            dest_fee: TokenAmount | None = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        failed_text = f'Failed to send {self.client.network.name} USDC to {to_network.name} USDC via Stargate'
        # try:
        if self.client.network.name == to_network.name:
            return f'{failed_text}: The same source network and destination network'

        usdc_contract = await self.client.contracts.default_token(
            contract_address=Stargate.contract_data[self.client.network.name]['usdc_contract'].address)
        stargate_contract = await self.client.contracts.get(
            contract_address=Stargate.contract_data[self.client.network.name]['stargate_contract'])

        if not amount:
            amount = await self.client.wallet.balance(token=usdc_contract.address)

        lz_tx_params = TxArgs(
            dstGasForCall=0,
            dstNativeAmount=dest_fee.Wei if dest_fee else 0,
            dstNativeAddr=self.client.account.address if dest_fee else '0x0000000000000000000000000000000000000001'
        )

        args = TxArgs(
            _dstChainId=Stargate.contract_data[to_network.name]['stargate_chain_id'],
            _srcPoolId=Stargate.contract_data[to_network.name]['src_pool_id'],
            _dstPoolId=Stargate.contract_data[to_network.name]['dst_pool_id'],
            _refundAddress=self.client.account.address,
            _amountLD=amount.Wei,
            _minAmountLD=int(amount.Wei * (100 - slippage) / 100),
            _lzTxParams=lz_tx_params.tuple(),
            _to=self.client.account.address,
            _payload='0x'
        )

        value = await self.get_value(
            router_contract=stargate_contract,
            to_network=to_network,
            lz_tx_params=lz_tx_params
        )
        if not value:
            return f'{failed_text} | can not get value ({self.client.network.name})'

        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text}: To low native balance: balance: {native_balance.Ether}; value: {value.Ether}'

        token_price = await self.get_token_price(token_symbol=self.client.network.coin_symbol)

        dst_native_amount_dollar = 0
        if dest_fee:
            dest_native_token_price = await self.get_token_price(token_symbol=to_network.coin_symbol)
            dst_native_amount_dollar = float(dest_fee.Ether) * dest_native_token_price

        network_fee = float(value.Ether) * token_price
        if network_fee - dst_native_amount_dollar > max_fee:
            return (f'{failed_text} | too high fee: {network_fee - dst_native_amount_dollar} '
                    f'({self.client.network.name})')

        if await self.approve_interface(
                token_address=usdc_contract.address,
                spender=stargate_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | Can not approve'

        tx_params = TxParams(
            to=stargate_contract.address,
            data=stargate_contract.encodeABI('swap', args=args.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return (f'{amount.Ether} USDC was send from {self.client.network.name} to {to_network.name} '
                    f'via Stargate: {tx.hash.hex()}')
        return f'{failed_text}!'

        # except Exception as e:
        #     return f'{failed_text}: {e}'

    async def get_value(self, router_contract: AsyncContract, to_network: Network,
                        lz_tx_params: TxArgs) -> TokenAmount | None:
        res = await router_contract.functions.quoteLayerZeroFee(
            Stargate.contract_data[to_network.name]['stargate_chain_id'],
            1,
            self.client.w3.to_bytes(text=self.client.account.address),
            self.client.w3.to_bytes(text='0x'),
            lz_tx_params.list()
        ).call()
        return TokenAmount(amount=res[0], wei=True)

    @staticmethod
    async def get_network_with_max_usdc_balance(
            address: ChecksumAddress,
    ) -> Network | None:
        supported_networks = [Networks.Avalanche, Networks.Polygon, Networks.Optimism, Networks.Arbitrum]

        result_network = None
        max_balance = TokenAmount(amount=0)
        for network in supported_networks:
            client = Client(network=network)
            usdc_balance = await client.wallet.balance(
                token=Stargate.contract_data[network.name]['usdc_contract'], address=address)
            if float(usdc_balance.Ether) > float(max_balance.Ether):
                max_balance = usdc_balance
                result_network = network
        return result_network
