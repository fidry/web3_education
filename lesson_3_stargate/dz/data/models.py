from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.utils import read_json
from eth_async.classes import Singleton

from data.config import ABIS_DIR


class Contracts(Singleton):
    # Arbitrum
    ARBITRUM_WOOFI = RawContract(
        title="WooFi",
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30',
        abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        title='USDC',
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        abi=DefaultABIs.Token
    )

    ARBITRUM_USDC_e = RawContract(
        title='USDC_e',
        address='0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract(
        title='ETH',
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        abi=DefaultABIs.Token
    )

    ARBITRUM_ARB = RawContract(
        title='ARB',
        address='0x912CE59144191C1204E64559FE8253a0e49E6548',
        abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        title='WBTC',
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f',
        abi=DefaultABIs.Token
    )

    ARBITRUM_STARGATE = RawContract(
        title='arbitrum_stargate',
        address='0x53bf833a5d6c4dda888f69c22c88c9f356a41614',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_STARGATE = RawContract(
        title='polygon_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_USDC = RawContract(
        title='USDC',
        address='0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        abi=DefaultABIs.Token
    )

    AVALANCHE_STARGATE = RawContract(
        title='avalanchen_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_USDC = RawContract(
        title='USDC',
        address='0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        abi=DefaultABIs.Token
    )

    OPTIMISM_USDC = RawContract(
        title='USDC',
        address='0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
        abi=DefaultABIs.Token
    )

    OPTIMISM_STARGATE = RawContract(
        title='optimism_stargate',
        address='0xb0d502e938ed5f4df2e681fe6e419ff29631d62b',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )
