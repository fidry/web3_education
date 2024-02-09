import json

from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.utils import read_json
from eth_async.classes import Singleton

from data.config import ABIS_DIR


OfficialBridgeZkSyncABI = [
    {
        'constant': False,
        'inputs': [
            {'name': '_l1Receiver', 'type': 'address'},
        ],
        'name': 'withdraw',
        'outputs': [],
        'payable': True,
        'stateMutability': 'payable',
        'type': 'function'
    }
]


class Contracts(Singleton):
    ETH_OFFICIAL_BRIDGE = RawContract(
        title='ETH_OFFICIAL_BRIDGE',
        address='0x32400084c286cf3e17e7b677ea9583e60a000324',
        abi=read_json(path=(ABIS_DIR, 'official_bridge.json'))
    )

    # zkSync
    ZKSYNC_OFFICIAL_BRIDGE = RawContract(
        title='ZKSYNC_OFFICIAL_BRIDGE',
        address='0x000000000000000000000000000000000000800A',
        abi=json.dumps(OfficialBridgeZkSyncABI)
    )

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

    # SyncSwap pool addresses
    SYNCSWAP_ETH_USDC_POOL = RawContract(
        address='0x80115c708E12eDd42E504c1cD52Aea96C547c05c'
    )
    SYNCSWAP_ETH_USDT_POOL = RawContract(
        address='0xd3D91634Cf4C04aD1B76cE2c06F7385A897F54D3'
    )
    SYNCSWAP_ETH_BUSD_POOL = RawContract(
        address='0xad86486f1d225d624443e5df4b2301d03bbe70f6'
    )
    SYNCSWAP_ETH_WBTC_POOL = RawContract(
        address='0xb3479139e07568ba954c8a14d5a8b3466e35533d'
    )
