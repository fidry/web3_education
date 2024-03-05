'''
stake 0.2 APT: https://explorer.aptoslabs.com/txn/0xeaf73be210cf3b65f26ae5598c65f7008ebff6bcbaa6d73b2eafb38783196bab?network=mainnet
'''

from tasks.stake import Stake
from data.models import TokenAmount, StakeRouters


class Tortuga(Stake):
    def stake(self, amount_in: TokenAmount):
        dex = StakeRouters.Tortuga
        return super()._stake(dex=dex, amount_in=amount_in)
