from web3 import types
from web3.contract import AsyncContract

from .models import RawContract, TokenAmount

Contract = str | types.Address | types.ChecksumAddress | types.ENS | RawContract | AsyncContract
Address = str | types.Address | types.ChecksumAddress | types.ENS
Amount = float | int | TokenAmount
GasPrice = int | TokenAmount
GasLimit = int | TokenAmount
