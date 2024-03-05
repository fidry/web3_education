from typing import Optional
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    TransactionArgument,
)
from aptos_sdk.bcs import Serializer

from client import AptosClient
from data.models import Token, TokenAmount, SwapRouters
from data.config import logger
from utils.utils import get_explorer_hash_link
from tasks.base import Base


class PancakeSwap(Base):
    def swap(
            self,
            from_token: Token,
            to_token: Token,
            amount_in: Optional[TokenAmount] = None,
            loss_ratio: float = 0.99,
    ) -> str:
        dex = SwapRouters.PancakeSwap
        failed_text = f'Failed to swap {from_token.name} to {to_token.name} via {dex.name}'
        logger.info(f'Start swap {from_token.name} to {to_token.name} via {dex.name}')
        try:
            if not amount_in:
                amount_in = self.aptos_client.get_balance(token=from_token)

            simulation_payload = EntryFunction.natural(
                dex.script,
                dex.function,
                AptosClient.get_type_args(dex=dex, from_token=from_token, to_token=to_token),
                [
                    TransactionArgument(amount_in.Wei, Serializer.u64),
                    TransactionArgument(0, Serializer.u64),
                ]
            )

            tx = self.aptos_client.create_bcs_transaction(
                self.aptos_client.signer, TransactionPayload(simulation_payload)
            )
            simulation = self.aptos_client.simulate_transaction(tx, self.aptos_client.signer)
            events = simulation[0]['events']
            if events:
                amount_out = int(int(events[-1]['data']['amount_x_out']) * loss_ratio)
            else:
                amount_out = float(self.aptos_client.get_token_price(
                    amount_in=amount_in,
                    from_token=from_token,
                    to_token=to_token
                ).Ether)
                amount_out = int(amount_out * loss_ratio)

            payload = EntryFunction.natural(
                dex.script,
                dex.function,
                self.aptos_client.get_type_args(dex, from_token, to_token),
                [
                    TransactionArgument(amount_in.Wei, Serializer.u64),
                    TransactionArgument(amount_out, Serializer.u64),
                ]
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
