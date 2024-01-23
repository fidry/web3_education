'''
Arbitrum:
arbitrum -> avalanche (2.5): https://arbiscan.io/tx/0x3ad0c8aa2b5675c3f6fbfde5fb6c668c95a99179db0b9f107a6068c7bfe0071b
arbitrum -> polygon (2.5): https://arbiscan.io/tx/0xad55c727e33ded6bfca74417705cebb31d307430b1da8dc8a17b02225e5a462a

Polygon:
polygon -> arbitrum (1): https://polygonscan.com/tx/0xc14084044d5abccb11647c9f6a6b2fa68df4551b828326d345bf27e77d755e38
polygon -> avalanche (1): https://polygonscan.com/tx/0x432b5592bb9bfdce14845844bd09c3bed9fc6bb54311608142ca60469e819346

Avalanche:
avalanche -> arbitrum (1): https://snowtrace.io/tx/0x0d14541440bf7731070649f9447365b61f7760b3f8895f8fa544265869a76e3c
avalanche -> polygon (1): https://snowtrace.io/tx/0x4716dcfa604b5e11cc8c930ecef8f7f0c42f05bd31d1eb1401c84fe798af9395

avalanche -> bsc (2.5 USDT): https://snowtrace.io/tx/0x47d2cfa1d89b1656c83c5548e0b5fd17cc54ea8f4674b3f02d0c324546778d53
'''


from tasks.base import Base
from eth_async.models import Networks, Network, TokenAmount

from data.models import Contracts


class Stargate(Base):
    contract_data = {
        Networks.Arbitrum.name: {
            'usdc_contract': Contracts.ARBITRUM_USDC_e,
            'stargate_contract': Contracts.ARBITRUM_STARGATE,
            'stargate_chain_id': 110,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Avalanche.name: {
            'usdc_contract': Contracts.AVALANCHE_USDC,
            'stargate_contract': Contracts.ALAVANCHE_STARGATE,
            'stargate_chain_id': 106,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Polygon.name: {
            'usdc_contract': Contracts.POLYGON_USDC,
            'stargate_contract': Contracts.POLYGON_STARGATE,
            'stargate_chain_id': 102,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
    }

    def send_usdc(
            self,
            to_network: Network,
            amount: TokenAmount | None = None,
            slippage: float = 0.5,
            max_fee: float = 1,
    ):
        ...
