from decimal import Decimal
from typing import Union, Optional
from dataclasses import dataclass


class ResourceType:
    # https://aptos.dev/integration/aptos-api/
    info = '0x1::coin::CoinInfo'
    store = '0x1::coin::CoinStore'
    token_store = '0x3::token::TokenStore'


class Token:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def __str__(self) -> str:
        return f'{self.name}'


class Tokens:
    # https://coinmarketcap.com/coins/
    APT = Token(
        name='AptosCoin', address='0x1::aptos_coin::AptosCoin')
    LZ_USDT = Token(
        name='USDT', address='0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDT')
    LZ_USDC = Token(
        name='USDC', address='0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC')
    LZ_WETH = Token(
        name='WETH', address='0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::WETH')
    WH_USDC = Token(
        name='T', address='0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T')
    LP_TORTUGA = Token(
        name='StakedAptosCoin', address='0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin')
    LP_DITTO = Token(
        name='StakedAptos',
        address='0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos')

    TOKENS_LIST = [APT, LZ_USDT, LZ_USDC, LZ_WETH, WH_USDC]
    LP_TOKENS_LIST = [LP_TORTUGA, LP_DITTO]


class RouterInfo:
    def __init__(self, name: str, module_account: str, script: str, function: str):
        self.name = name
        self.module_account = module_account
        self.script = script
        self.function = function

    def __str__(self) -> str:
        return f'{self.name}'


class DomainNameInfo:
    def __init__(self, name: str, script: str, function: str):
        self.name = name
        self.script = script
        self.function = function

    def __str__(self) -> str:
        return f'{self.name}'


class StakeRouterInfo(RouterInfo):
    pass


class SwapRouterInfo(RouterInfo):
    # todo: поменять название resource_type, script, resource_account
    def __init__(self, name: str,  module_account: str, script: str, function: str,
                 resource_type: str, resource_account: str, curve_uncorrelated: Optional[str] = None):
        super().__init__(name=name, module_account=module_account, function=function, script=script)
        self.resource_type = resource_type
        self.resource_account = resource_account
        self.curve_uncorrelated = curve_uncorrelated


class SwapRouters:
    pancakeswap_module_account = '0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa'
    liquidswap_module_account = '0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12'

    PancakeSwap = SwapRouterInfo(
        name='pancakeswap',
        module_account=pancakeswap_module_account,
        script=f'{pancakeswap_module_account}::router',
        function='swap_exact_input',
        resource_type=f'{pancakeswap_module_account}::swap::TokenPairReserve',
        resource_account=pancakeswap_module_account,
    )

    LiquidSwap = SwapRouterInfo(
        name='liquidswap',
        module_account=liquidswap_module_account,
        script=f'{liquidswap_module_account}::scripts_v2',
        function='swap',
        resource_type=f'{liquidswap_module_account}::liquidity_pool::LiquidityPool',
        resource_account='0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948',
        # https://github.com/pontem-network/liquidswap/releases
        curve_uncorrelated=f'{liquidswap_module_account}::curves::Uncorrelated'
    )


class StakeRouters:
    tortuga_module_account = '0x8f396e4246b2ba87b51c0739ef5ea4f26515a98375308c31ac2ec1e42142a57f'
    ditto_module_account = '0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5'

    Tortuga = StakeRouterInfo(
        name='tortuga',
        module_account=tortuga_module_account,
        script=f'{tortuga_module_account}::stake_router',
        function='stake',
    )

    Ditto = StakeRouterInfo(
        name='ditto',
        module_account=ditto_module_account,
        script=f'{ditto_module_account}::ditto_staking',
        function='stake_aptos',
    )


class DomainNamesInfo:
    router = "0x867ed1f6bf916171b1de3ee92849b8978b7d1b9e0a8cc982a3d19d535dfd9c0c"

    AptosNamesOld = DomainNameInfo(
        name='aptos_names_old',
        script=f'{router}::domains',
        function='register_domain_with_signature'
    )

    AptosNames = DomainNameInfo(
        name='aptos_names',
        script=f'{router}::router',
        function='register_domain'
    )


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


class Tx:
    def __init__(
            self,
            version: str,
            tx_hash: str,
            success: bool,
            changes: Optional[list] = None,
            sender: Optional[str] = None,
            nonce: Union[str, int, None] = None,
            max_gas_amount: Optional[int] = None,
            gas_unit_price: Optional[int] = None,
            payload: Optional[dict] = None,
            signature: Optional[dict] = None,
            events: Optional[list] = None,
            tx_type: Optional[str] = None,
    ):
        self.version = version
        self.tx_hash = tx_hash
        self.success = success
        self.changes = changes
        self.sender = sender
        self.nonce = nonce
        self.max_gas_amount = max_gas_amount
        self.gas_unit_price = gas_unit_price
        self.payload = payload
        self.signature = signature
        self.events = events
        self.tx_type = tx_type

        if self.nonce:
            self.nonce = int(self.nonce)
        if self.max_gas_amount:
            self.max_gas_amount = int(self.max_gas_amount)
        if self.gas_unit_price:
            self.gas_unit_price = int(self.gas_unit_price)

    def __str__(self):
        return f'{self.tx_hash}'


@dataclass
class FromTo:
    from_: Union[int, float]
    to_: Union[int, float]


class AutoRepr:
    def __repr__(self) -> str:
        values = ('{}={!r}'.format(key, value) for key, value in vars(self).items())
        return '{}({})'.format(self.__class__.__name__, ', '.join(values))


class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)

        return cls._instances[cls]


class DomainNamesModel:
    captcha_key: str
    google_key: str
