import os
from decimal import Decimal
from typing import Union
import json

from data.config import ABIS_DIR

ETH_ADDRESS = int('0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7', 16)
DAI_ADDRESS = int('0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3', 16)
USDC_ADDRESS = int('0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8', 16)
USDT_ADDRESS = int('0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8', 16)
MY_SWAP_ROUTER = int('0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28', 16)

DEFAULT_TOKEN_ABI = json.load(open(os.path.join(ABIS_DIR, 'default_token_abi.json')))


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        """
        A token amount instance.
        :param Union[int, float, str, Decimal] amount: an amount
        :param int decimals: the decimals of the token (18)
        :param bool wei: the 'amount' is specified in Wei (False)
        """
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals

    def __str__(self):
        return f'{self.Ether}'
