from bybit.models import ByBitCredentials
from py_okx_async.models import OKXCredentials


bybit_api_key = ''
bybit_secret_key = ''

okx_api_key = ''
okx_secret_key = ''
okx_passphrase = ''

bybit_credentials = ByBitCredentials(api_key=bybit_api_key, api_secret=bybit_secret_key)

okx_credentials = OKXCredentials(
    api_key=okx_api_key,
    secret_key=okx_secret_key,
    passphrase=okx_passphrase
)
