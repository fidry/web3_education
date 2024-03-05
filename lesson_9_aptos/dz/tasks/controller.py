from data.models import Tokens, SwapRouters, StakeRouters
from client import AptosClient
from tasks.base import Base
from tasks.liquidswap import Liquidswap
from tasks.pancakeswap import PancakeSwap
from tasks.tortuga import Tortuga
from tasks.ditto import Ditto
from tasks.domain_names import DomainNames


class Controller(Base):
    def __init__(self, aptos_client: AptosClient):
        super().__init__(aptos_client=aptos_client)
        self.pancakeswap = PancakeSwap(aptos_client=aptos_client)
        self.liquidswap = Liquidswap(aptos_client=aptos_client)
        self.tortuga = Tortuga(aptos_client=aptos_client)
        self.ditto = Ditto(aptos_client=aptos_client)
        self.domain_names = DomainNames(aptos_client=aptos_client)

    def collect_all_tokens_to_apt(self):
        tokens = self.aptos_client.get_account_tokens()
        try:
            for token in tokens:
                if token.name == Tokens.APT.name:
                    continue
                balance = self.aptos_client.get_balance(token)
                if balance.Wei > 0:
                    self.liquidswap.swap(from_token=token, to_token=Tokens.APT)
        except Exception:
            return False
        return True

    def count_swaps(self):
        swaps = 0
        txs = self.aptos_client.get_tx_list()
        for tx in txs:
            function = tx.payload.get('function')
            if not function:
                continue
            if SwapRouters.LiquidSwap.script + '::' + SwapRouters.LiquidSwap.function in function or \
                    SwapRouters.PancakeSwap.script + '::' + SwapRouters.PancakeSwap.function in function:
                swaps += 1
        return swaps

    def count_stakes(self):
        stakes = 0
        txs = self.aptos_client.get_tx_list()
        for tx in txs:
            function = tx.payload.get('function')
            if not function:
                continue
            if StakeRouters.Tortuga.script + '::' + StakeRouters.Tortuga.function in function or \
                    StakeRouters.Ditto.script + '::' + StakeRouters.Ditto.function in function:
                stakes += 1
        return stakes
