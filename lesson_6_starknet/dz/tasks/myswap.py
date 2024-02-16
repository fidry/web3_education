from starknet_py.contract import Contract

from data import models
from data.models import TokenAmount, DEFAULT_TOKEN_ABI
from tasks.base import Base


class MySwap(Base):
    # transaction example: https://starkscan.co/tx/0x002bf5229598d98b4ef838f1f8e9b5009dbeb0d0e4c658bd8d46f396c76e04e1

    CONTRACT_MAP = {
        'USDC': {
            'token_address': models.USDC_ADDRESS,
            'pool_id': 1
        },
        'DAI': {
            'token_address': models.DAI_ADDRESS,
            'pool_id': 2
        },
        'USDT': {
            'token_address': models.USDT_ADDRESS,
            'pool_id': 4
        },
    }

    async def swap_eth_to_token(self, amount_in: TokenAmount, token_out_name: str):
        token_out_name = token_out_name.upper()

        token_address = MySwap.CONTRACT_MAP[token_out_name]['token_address']
        pool_id = MySwap.CONTRACT_MAP[token_out_name]['pool_id']

        token_out_decimals = await self.starknet_client.get_decimals(token_address)
        amount_out = await Base.get_amount_out(
            amount_in=amount_in,
            token_out_name=token_out_name,
            amount_out_decimals=token_out_decimals
        )

        eth_contract = Contract(
            address=models.ETH_ADDRESS,
            abi=DEFAULT_TOKEN_ABI,
            provider=self.starknet_client.account,
        )
        myswap_contract = await Contract.from_address(
            address=models.MY_SWAP_ROUTER,
            provider=self.starknet_client.account,
            proxy_config=True
        )

        approve_call = eth_contract.functions["approve"].prepare_call(
            spender=models.MY_SWAP_ROUTER,
            amount=amount_in.Wei
        )
        swap_call = myswap_contract.functions["swap"].prepare_call(
            pool_id=pool_id,
            token_from_addr=models.ETH_ADDRESS,
            amount_from=amount_in.Wei,
            amount_to_min=amount_out.Wei
        )

        response = await self.starknet_client.account.execute_v1(
            calls=[approve_call, swap_call],
            auto_estimate=True,
        )

        decimal_value = response.transaction_hash
        hex_value = '0x0' + hex(decimal_value)[2:]
        print(f'\n>>>> MySwap transaction | https://starkscan.co/tx/{hex_value}')
        tx_res = await self.starknet_client.account.client.wait_for_tx(
            response.transaction_hash
        )
        return tx_res

    async def swap_token_to_eth(self, token_in_name: str, amount_in: TokenAmount | None = None):
        token_in_name = token_in_name.upper()

        token_address = MySwap.CONTRACT_MAP[token_in_name]['token_address']
        pool_id = MySwap.CONTRACT_MAP[token_in_name]['pool_id']

        if not amount_in:
            amount_in = await self.starknet_client.get_balance(token_address=token_address)

        token_in_decimals = await self.starknet_client.get_decimals(token_address)

        amount_out = await Base.get_amount_out(
            amount_in=amount_in,
            token_in_name=token_in_name,
            token_out_name='ETH',
            amount_out_decimals=token_in_decimals
        )

        token_contract = Contract(
            address=token_address,
            abi=DEFAULT_TOKEN_ABI,
            provider=self.starknet_client.account,
        )
        myswap_contract = await Contract.from_address(
            address=models.MY_SWAP_ROUTER,
            provider=self.starknet_client.account,
            proxy_config=True
        )

        approve_call = token_contract.functions["approve"].prepare_call(
            spender=models.MY_SWAP_ROUTER,
            amount=amount_in.Wei
        )
        swap_call = myswap_contract.functions["swap"].prepare_call(
            pool_id=pool_id,
            token_from_addr=token_address,
            amount_from=amount_in.Wei,
            amount_to_min=amount_out.Wei
        )

        response = await self.starknet_client.account.execute_v1(
            calls=[approve_call, swap_call],
            auto_estimate=True
        )
        decimal_value = response.transaction_hash
        hex_value = '0x0' + hex(decimal_value)[2:]
        print(f'\n>>>> MySwap transaction | https://starkscan.co/tx/{hex_value}')
        tx_res = await self.starknet_client.account.client.wait_for_tx(
            response.transaction_hash
        )
        return tx_res
