import asyncio
from typing import Optional
from web3.types import TxParams
from eth_async.models import TxArgs, TokenAmount

from data.models import Contracts, RawContract
from tasks.base import Base


class WooFi(Base):
    async def swap(
            self,
            from_token: RawContract,
            to_token: RawContract,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        # 1 способ получения имени нативной монеты
        from_token_symbol = from_token.title
        to_token_symbol = to_token.title

        # 2 способ получения имени нативной монеты
        # from_token_contract = await self.client.contracts.default_token(from_token.address)
        # to_token_contract = await self.client.contracts.default_token(to_token.address)
        # from_token_symbol = await from_token_contract.functions.symbol().call()
        # to_token_symbol = await to_token_contract.functions.symbol().call() \
        #     if to_token.address != Contracts.ARBITRUM_ETH.address else to_token.title

        failed_text = f'Failed swap {from_token_symbol} to {to_token_symbol} via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token.address)

        if from_token != Contracts.ARBITRUM_ETH:
            if await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount):
                await asyncio.sleep(1)
            else:
                return f'{failed_text}: Can not approve'

        from_token_price = await self.get_token_price(token_symbol=from_token_symbol)
        to_token_price = await self.get_token_price(token_symbol=to_token_symbol)

        # todo: убрать костыль
        if to_token == Contracts.ARBITRUM_ETH:
            decimals = 18
        else:
            decimals = await self.client.transactions.get_decimals(contract=to_token)

        min_to_amount = TokenAmount(
            amount=float(amount.Ether) * (from_token_price / to_token_price) * (1 - slippage / 100),
            decimals=decimals
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
        )
        if from_token == Contracts.ARBITRUM_ETH:
            tx_params['value'] = amount.Wei

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return (f'{amount.Ether} {from_token_symbol} was swaped to '
                    f'{min_to_amount.Ether} {to_token_symbol} via WooFi: {tx.hash.hex()}')

        return f'{failed_text}!'
