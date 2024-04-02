from libs.eth_async.client import Client
from libs.eth_async.data.models import Networks
from zksync_explorer.explorer_api import APIFunctions
from data.models import Contracts, Settings
from tasks.base import Base
from tasks.maverick import Maverick
from tasks.mute import Mute
from tasks.space_fi import SpaceFi
from tasks.syncswap import SyncSwap
from tasks.dmail import Dmail
from tasks.official_bridge import OfficialBridge


class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client)

        self.base = Base(client=client)
        self.official_bridge = OfficialBridge(client=client)
        self.maverick = Maverick(client=client)
        self.mute = Mute(client=client)
        self.space_fi = SpaceFi(client=client)
        self.syncswap = SyncSwap(client=client)
        self.dmail = Dmail(client=client)

    async def made_ethereum_bridge(self) -> bool:
        client = Client(private_key='', network=Networks.Ethereum)
        return bool(await client.transactions.find_txs(
            contract=Contracts.ETH_OFFICIAL_BRIDGE,
            function_name='requestL2Transaction',
            address=self.client.account.address,
        ))

    async def count_swaps(self, tx_list: list[dict] | None = None):
        settings = Settings()
        result_count = 0

        api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)

        if not tx_list:
            tx_list = await api_oklink.account.txlist_all(
                address=self.client.account.address
            )

        # Maveric
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.MAVERICK.address,
            method_id='0xac9650d8',
            tx_list=tx_list
        ))

        # Mute eth -> token
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.MUTE.address,
            method_id='0x51cbf10f',
            tx_list=tx_list
        ))

        # Mute token -> eth
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.MUTE.address,
            method_id='0x3f464b16',
            tx_list=tx_list
        ))

        # SpaceFi eth -> token
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.SPACE_FI.address,
            method_id='0x7ff36ab5',
            tx_list=tx_list
        ))

        # SpaceFi token -> eth
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.SPACE_FI.address,
            method_id='0x18cbafe5',
            tx_list=tx_list
        ))

        # SyncSwap
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.SYNC_SWAP.address,
            method_id='0x2cc4081e',
            tx_list=tx_list
        ))

        return result_count

    async def count_dmail(self, tx_list: list[dict] | None = None):
        settings = Settings()
        result_count = 0

        api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)

        if not tx_list:
            tx_list = await api_oklink.account.txlist_all(
                address=self.client.account.address
            )

        # dmail
        result_count += len(await api_oklink.account.find_tx_by_method_id(
            address=self.client.account.address,
            to=Contracts.DMAIL.address,
            method_id='0x5b7d7482',
            tx_list=tx_list
        ))

        return result_count

    async def count_liquidity(self, txs: list[dict] | None = None):
        # todo: посчитать количество транзакций на добавление ликвидности в syncswap
        ...
