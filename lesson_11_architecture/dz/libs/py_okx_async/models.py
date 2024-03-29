from dataclasses import dataclass


class ReprWithoutData:
    """
    Contains a __repr__ function that automatically builds the output of a class using all its variables except 'data'.
    """

    def __repr__(self) -> str:
        attributes = vars(self).copy()
        del attributes['data']
        values = ('{}={!r}'.format(key, value) for key, value in attributes.items())
        return '{}({})'.format(self.__class__.__name__, ', '.join(values))


@dataclass
class StateName:
    """
    An instance with state and name attributes.

    Attributes:
        state (str): a state.
        name (str): a name.

    """
    state: str
    name: str


@dataclass
class OKXCredentials:
    """
    An instance that contains OKX API key data.

    Attributes:
        api_key (str): an API key.
        secret_key (str): a secret key.
        passphrase (str): a passphrase.

    """
    api_key: str
    secret_key: str
    passphrase: str

    def completely_filled(self) -> bool:
        """
        Check if all required attributes are specified.

        Returns:
            bool: True if all required attributes are specified.

        """
        return all((self.api_key, self.secret_key, self.passphrase))


class Methods:
    """
    An instance with names of HTTP request methods.
    """
    GET = 'GET'
    POST = 'POST'


class Chains:
    """
    An instance with all chain names supported by OKX.
    """
    AELF = 'AELF'
    Acala = 'Acala'
    Algorand = 'Algorand'
    Aptos = 'Aptos'
    ArbitrumOne = 'Arbitrum One'
    ArbitrumOneBridged = 'Arbitrum One (Bridged)'
    Arweave = 'Arweave'
    Astar = 'Astar'
    AvalancheCChain = 'Avalanche C-Chain'
    AvalancheXChain = 'Avalanche X-Chain'
    BRC20 = 'BRC20'
    BSC = 'BSC'
    Bitcoin = 'Bitcoin'
    BitcoinSV = 'Bitcoin SV'
    BitcoinCash = 'BitcoinCash'
    Bytom = 'Bytom'
    CELO = 'CELO'
    CELOTOKEN = 'CELO-TOKEN'
    CFX_EVM = 'CFX_EVM'
    CORE = 'CORE'
    Cardano = 'Cardano'
    Casper = 'Casper'
    Chia = 'Chia'
    ChilizLegacyChain = 'Chiliz Legacy Chain'
    Conflux = 'Conflux'
    Cortex = 'Cortex'
    Cosmos = 'Cosmos'
    Crypto = 'Crypto'
    Decred = 'Decred'
    Dfinity = 'Dfinity'
    Digibyte = 'Digibyte'
    DigitalCash = 'Digital Cash'
    Dogecoin = 'Dogecoin'
    EOS = 'EOS'
    ERC20 = 'ERC20'
    Elrond = 'Elrond'
    Eminer = 'Eminer'
    EthereumClassic = 'Ethereum Classic'
    EthereumPoW = 'EthereumPoW'
    FEVM = 'FEVM'
    FLOW = 'FLOW'
    Fantom = 'Fantom'
    Filecoin = 'Filecoin'
    Flare = 'Flare'
    Fusion = 'Fusion'
    Harmony = 'Harmony'
    Hedera = 'Hedera'
    Horizen = 'Horizen'
    HyperCash = 'HyperCash'
    ICON = 'ICON'
    INTCHAIN = 'INTCHAIN'
    IOST = 'IOST'
    KAR = 'KAR'
    Kadena = 'Kadena'
    Khala = 'Khala'
    Klaytn = 'Klaytn'
    Kusama = 'Kusama'
    Lightning = 'Lightning'
    Linkeye = 'Linkeye'
    Lisk = 'Lisk'
    Litecoin = 'Litecoin'
    MIOTA = 'MIOTA'
    Metis = 'Metis'
    Mina = 'Mina'
    Monero = 'Monero'
    Moonbeam = 'Moonbeam'
    Moonriver = 'Moonriver'
    N3 = 'N3'
    NEAR = 'NEAR'
    NEO = 'NEO'
    NULS = 'NULS'
    Nano = 'Nano'
    NewEconomyMovement = 'New Economy Movement'
    OASYS = 'OASYS'
    OKTC = 'OKTC'
    OmegaChain = 'Omega Chain'
    Ontology = 'Ontology'
    Optimism = 'Optimism'
    OptimismBridged = 'Optimism (Bridged)'
    OptimismV1 = 'Optimism (V1)'
    OptimismV2 = 'Optimism (V2)'
    PlatON = 'PlatON'
    Polkadot = 'Polkadot'
    Polygon = 'Polygon'
    Quantum = 'Quantum'
    Ravencoin = 'Ravencoin'
    Ripple = 'Ripple'
    Ronin = 'Ronin'
    SUI = 'SUI'
    Siacoin = 'Siacoin'
    Solana = 'Solana'
    Starknet = 'Starknet'
    StellarLumens = 'Stellar Lumens'
    StepNetwork = 'Step Network'
    TON = 'TON'
    TRC20 = 'TRC20'
    Terra = 'Terra'
    TerraClassic = 'Terra Classic'
    Tezos = 'Tezos'
    Theta = 'Theta'
    UMEE = 'UMEE'
    VSYSTEMS = 'VSYSTEMS'
    WAVES = 'WAVES'
    WGRT = 'WGRT'
    Wax = 'Wax'
    XANA = 'XANA'
    XEC = 'XEC'
    Zcash = 'Zcash'
    Zilliqa = 'Zilliqa'
    lStacks = 'l-Stacks'
    zkSyncEra = 'zkSync Era'
    zkSyncLite = 'zkSync Lite'

    all_chains = {
        'aelf': AELF,
        'acala': Acala,
        'algorand': Algorand,
        'aptos': Aptos,
        'arbitrum one': ArbitrumOne,
        'arbitrum one (bridged)': ArbitrumOneBridged,
        'arweave': Arweave,
        'astar': Astar,
        'avalanche c-chain': AvalancheCChain,
        'avalanche x-chain': AvalancheXChain,
        'brc20': BRC20,
        'bsc': BSC,
        'bitcoin': Bitcoin,
        'bitcoin sv': BitcoinSV,
        'bitcoincash': BitcoinCash,
        'bytom': Bytom,
        'celo': CELO,
        'celo-token': CELOTOKEN,
        'cfx_evm': CFX_EVM,
        'core': CORE,
        'cardano': Cardano,
        'casper': Casper,
        'chia': Chia,
        'chiliz legacy chain': ChilizLegacyChain,
        'conflux': Conflux,
        'cortex': Cortex,
        'cosmos': Cosmos,
        'crypto': Crypto,
        'decred': Decred,
        'dfinity': Dfinity,
        'digibyte': Digibyte,
        'digital cash': DigitalCash,
        'dogecoin': Dogecoin,
        'eos': EOS,
        'erc20': ERC20,
        'elrond': Elrond,
        'eminer': Eminer,
        'ethereum classic': EthereumClassic,
        'ethereumpow': EthereumPoW,
        'fevm': FEVM,
        'flow': FLOW,
        'fantom': Fantom,
        'filecoin': Filecoin,
        'flare': Flare,
        'fusion': Fusion,
        'harmony': Harmony,
        'hedera': Hedera,
        'horizen': Horizen,
        'hypercash': HyperCash,
        'icon': ICON,
        'intchain': INTCHAIN,
        'iost': IOST,
        'kar': KAR,
        'kadena': Kadena,
        'khala': Khala,
        'klaytn': Klaytn,
        'kusama': Kusama,
        'lightning': Lightning,
        'linkeye': Linkeye,
        'lisk': Lisk,
        'litecoin': Litecoin,
        'miota': MIOTA,
        'metis': Metis,
        'mina': Mina,
        'monero': Monero,
        'moonbeam': Moonbeam,
        'moonriver': Moonriver,
        'n3': N3,
        'near': NEAR,
        'neo': NEO,
        'nuls': NULS,
        'nano': Nano,
        'new economy movement': NewEconomyMovement,
        'oasys': OASYS,
        'oktc': OKTC,
        'omega chain': OmegaChain,
        'ontology': Ontology,
        'optimism': Optimism,
        'optimism (bridged)': OptimismBridged,
        'optimism (v1)': OptimismV1,
        'optimism (v2)': OptimismV2,
        'platon': PlatON,
        'polkadot': Polkadot,
        'polygon': Polygon,
        'quantum': Quantum,
        'ravencoin': Ravencoin,
        'ripple': Ripple,
        'ronin': Ronin,
        'sui': SUI,
        'siacoin': Siacoin,
        'solana': Solana,
        'starknet': Starknet,
        'stellar lumens': StellarLumens,
        'step network': StepNetwork,
        'ton': TON,
        'trc20': TRC20,
        'terra': Terra,
        'terra classic': TerraClassic,
        'tezos': Tezos,
        'theta': Theta,
        'umee': 'UMEE',
        'vsystems': VSYSTEMS,
        'waves': WAVES,
        'wgrt': WGRT,
        'wax': Wax,
        'xana': XANA,
        'xec': XEC,
        'zcash': Zcash,
        'zilliqa': Zilliqa,
        'l-stacks': lStacks,
        'zksync era': zkSyncEra,
        'zksync lite': zkSyncLite
    }

    @staticmethod
    def are_equal(chain_1: str, chain_2: str) -> bool:
        """
        Compare if the names of chains match in lowercase.

        Args:
            chain_1 (str): the first chain name.
            chain_2 (str): the second chain name.

        Returns:
            bool: True if chains are equal.

        """
        return chain_1.lower() == chain_2.lower()


class FundingToken(ReprWithoutData):
    """
    An instance of a funding token.

    Attributes:
        data (dict[str, ...]): the raw data.
        token_symbol (str): token symbol, e.g. BTC.
        bal (float): balance.
        frozenBal (float): frozen balance.
        availBal (float): available balance. The balance that can be withdrawn or transferred or used for spot trading.

    """

    def __init__(self, data: dict[str, ...]) -> None:
        """
        Initialize the class.

        Args:
            data (dict[str, ...]): the dictionary with a funding token data.

        """
        self.data: dict[str, ...] = data
        self.token_symbol: str = data.get('ccy')
        self.bal: float = float(data.get('bal'))
        self.availBal: float = float(data.get('availBal'))
        self.frozenBal: float = float(data.get('frozenBal'))


@dataclass
class AccountType(StateName):
    """
    An instance of an account type.
    """
    pass


class AccountTypes:
    """
    An instance with all account types.
    """
    Funding = AccountType(state='6', name='funding')
    Trading = AccountType(state='18', name='trading')

    types_dict = {
        '6': Funding,
        '18': Trading
    }
