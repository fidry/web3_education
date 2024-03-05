import random
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    TransactionArgument,
)
from aptos_sdk.bcs import Serializer

from data.models import TokenAmount, StakeRouterInfo, Tokens, StakeRouters
from data.config import logger
from utils.utils import get_explorer_hash_link
from tasks.base import Base


class Stake(Base):
    def _stake(
            self,
            dex: StakeRouterInfo,
            amount_in: TokenAmount
    ):
        failed_text = f'Failed to stake {Tokens.APT.name} on {dex.name}'
        logger.info(f'Start stake {Tokens.APT.name} on {dex.name}')
        try:
            if dex.name == StakeRouters.Tortuga.name:
                additional_gas = self.aptos_client.client_config.max_gas_amount + random.randint(8000, 10000)
                self.aptos_client.client_config.max_gas_amount = additional_gas

            apt_balance = self.aptos_client.get_balance()

            if apt_balance.Wei < amount_in.Wei:
                return f'{failed_text}: Wallet balance ({apt_balance.Ether}) less than ' \
                       f'amount to stake ({amount_in.Ether})'

            payload = EntryFunction.natural(
                dex.script,
                dex.function,
                [],
                [TransactionArgument(amount_in.Wei, Serializer.u64)],
            )

            signed_transaction = self.aptos_client.create_bcs_signed_transaction(
                self.aptos_client.signer,
                TransactionPayload(payload)
            )

            tx = self.aptos_client.submit_bcs_transaction(signed_transaction)
            self.aptos_client.wait_for_transaction(tx)
            return f'{amount_in.Ether} {Tokens.APT.name} was staked on ' \
                   f'{dex.name}; hash: {get_explorer_hash_link(tx)}'

        except Exception as e:
            if "Out of gas" in str(e):
                return f'{failed_text}: Out of gas ({e})'
            return f'{failed_text}: something went wrong: ({e})'
