from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.utils import read_json
from eth_async.classes import Singleton

from data.config import ABIS_DIR


class Contracts(Singleton):
    MUTE = RawContract(
        title='mute',
        address='0x8b791913eb07c32779a16750e3868aa8495f5964',
        abi=read_json(path=(ABIS_DIR, 'mute.json'))
    )

    SPACE_FI = RawContract(
        title='space_fi',
        address='0xbe7d1fd1f6748bbdefc4fbacafbb11c6fc506d1d',
        abi=read_json(path=(ABIS_DIR, 'space_fi.json'))
    )

    SYNC_SWAP = RawContract(
        title='sync_swap',
        address='0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295',
        abi=read_json(path=(ABIS_DIR, 'syncswap.json'))
    )

    MAVERICK = RawContract(
        title='maverick',
        address='0x39E098A153Ad69834a9Dac32f0FCa92066aD03f4',
        abi=read_json(path=(ABIS_DIR, 'maverick.json'))
    )

    WETH = RawContract(
        title='WETH',
        address='0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91',
        abi=read_json(path=(ABIS_DIR, 'WETH.json'))
    )

    USDC = RawContract(
        title='USDC',
        address='0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4',
        abi=DefaultABIs.Token
    )

    WBTC = RawContract(
        title='WBTC',
        address='0xBBeB516fb02a01611cBBE0453Fe3c580D7281011',
        abi=DefaultABIs.Token
    )

    USDT = RawContract(
        title='USDT',
        address='0x493257fd37edb34451f62edf8d2a0c418852ba4c',
        abi=DefaultABIs.Token
    )

    ceBUSD = RawContract(
        title='ceBUSD',
        address='0x2039bb4116B4EFc145Ec4f0e2eA75012D6C0f181',
        abi=DefaultABIs.Token
    )
