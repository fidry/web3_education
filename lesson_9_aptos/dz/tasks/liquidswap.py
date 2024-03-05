from typing import Optional

from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    TransactionArgument,
)
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer

from client import AptosClient
from data.models import Token, TokenAmount, SwapRouters
from data.config import logger
from utils.utils import get_explorer_hash_link
from tasks.base import Base


class Liquidswap(Base):
    def swap(
            self,
            from_token: Token,
            to_token: Token,
            amount_in: Optional[TokenAmount] = None,
            loss_ratio: float = 0.99
    ) -> str:
        dex = SwapRouters.LiquidSwap
        failed_text = f'Failed to swap {from_token.name} to {to_token.name} via {dex.name}'
        logger.info(f'Start swap {from_token.name} to {to_token.name} via {dex.name}')
        try:
            if not amount_in:
                amount_in = self.aptos_client.get_balance(token=from_token)
            resource_account = AccountAddress.from_hex(dex.resource_account)

            try:
                resource_type = f"{dex.resource_type}<{from_token.address}, {to_token.address}, {dex.curve_uncorrelated}>"
                data = self.aptos_client.account_resource(
                    resource_type=resource_type,
                    account_address=resource_account
                )["data"]
                coin_x_reserve_value = int(data["coin_x_reserve"]["value"])
                coin_y_reserve_value = int(data["coin_y_reserve"]["value"])
            except:
                resource_type = f"{dex.resource_type}<{to_token.address}, {from_token.address}, {dex.curve_uncorrelated}>"
                data = self.aptos_client.account_resource(
                    resource_type=resource_type,
                    account_address=resource_account
                )["data"]
                coin_y_reserve_value = int(data["coin_x_reserve"]["value"])
                coin_x_reserve_value = int(data["coin_y_reserve"]["value"])

            from_token_decimals = self.aptos_client.get_decimals(from_token)
            to_token_decimals = self.aptos_client.get_decimals(to_token)
            reserve_x = TokenAmount(amount=coin_x_reserve_value, decimals=from_token_decimals, wei=True)
            reserve_y = TokenAmount(amount=coin_y_reserve_value, decimals=to_token_decimals, wei=True)

            amount_out = TokenAmount(
                amount=int(amount_in.Wei * reserve_y.Wei / reserve_x.Wei * loss_ratio),
                decimals=to_token_decimals,
                wei=True
            )

            payload = EntryFunction.natural(
                dex.script,
                dex.function,
                AptosClient.get_type_args(dex=dex, from_token=from_token, to_token=to_token),
                [
                    TransactionArgument(amount_in.Wei, Serializer.u64),
                    TransactionArgument(amount_out.Wei, Serializer.u64),
                ],
            )

            signed_transaction = self.aptos_client.create_bcs_signed_transaction(
                self.aptos_client.signer,
                TransactionPayload(payload)
            )

            tx = self.aptos_client.submit_bcs_transaction(signed_transaction)
            self.aptos_client.wait_for_transaction(tx)
            return f'{amount_in.Ether} {from_token.name} was swapped to ' \
                   f'{to_token.name} via {dex.name}; hash: {get_explorer_hash_link(tx)}'

        except Exception as e:
            if "ERR_COIN_OUT_NUM_LESS_THAN_EXPECTED_MINIMUM" in str(e):
                return f'{failed_text}: high loss_ratio'
            elif "INSUFFICIENT_BALANCE" in str(e):
                return f'{failed_text}: insufficient balance'
            return f'{failed_text}: something went wrong: {e}'
