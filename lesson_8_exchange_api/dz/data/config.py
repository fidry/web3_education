import os
import sys
from pathlib import Path

from py_okx_async.models import OKXCredentials


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()


ADDRESSES_PATH = os.path.join(ROOT_DIR, 'addresses.txt')
SUCCESS_ADDRESSES_PATH = os.path.join(ROOT_DIR, 'success_addresses.txt')
FAILED_ADDRESSES_PATH = os.path.join(ROOT_DIR, 'failed_addresses.txt')


okx_api_key = ''
okx_secret_key = ''
okx_passphrase = ''


okx_credentials = OKXCredentials(
    api_key=okx_api_key,
    secret_key=okx_secret_key,
    passphrase=okx_passphrase
)


maximum_gas_price = 60
withdraw_amount = {'from': 0.00105, 'to': 0.0015}
delay_between_withdrawals = {'from': 500, 'to': 600}
