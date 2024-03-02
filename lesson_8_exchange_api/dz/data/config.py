import os
import sys
from pathlib import Path

from bybit.models import ByBitCredentials
from py_okx_async.models import OKXCredentials


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ADDRESSES_PATH = os.path.join(ROOT_DIR, 'addresses.txt')

bybit_api_key = ''
bybit_secret_key = ''

okx_api_key = ''
okx_secret_key = ''
okx_passphrase = ''

bybit_credentials = ByBitCredentials(
    api_key=bybit_api_key,
    api_secret=bybit_secret_key
)

okx_credentials = OKXCredentials(
    api_key=okx_api_key,
    secret_key=okx_secret_key,
    passphrase=okx_passphrase
)

maximum_gas_price = 60
use_official_bridge = False
withdraw_amount_to_eth = {'from': 0.0001, 'to': 0.0002}
withdraw_amount_to_zksync = {'from': 0.0001, 'to': 0.0002}
delay_between_withdrawals = {'from': 60, 'to': 120}
