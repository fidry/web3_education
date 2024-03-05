'''
stake 0.2 APT: https://explorer.aptoslabs.com/txn/0x8dd2ef69ea00f2c8025d241624d3085a1cf78d1a5348b487a6b4b4750a49abc0?network=mainnet
'''

from tasks.stake import Stake
from data.models import TokenAmount, StakeRouters


class Ditto(Stake):
    def stake(self, amount_in: TokenAmount):
        dex = StakeRouters.Ditto
        return super()._stake(dex=dex, amount_in=amount_in)
