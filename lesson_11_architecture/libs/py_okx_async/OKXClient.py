import requests

from libs.py_okx_async.asset.Asset import Asset
from libs.py_okx_async.exceptions import InvalidProxy
from libs.py_okx_async.models import OKXCredentials
from libs.py_okx_async.subaccount.Subaccount import Subaccount


class OKXClient:
    """
    The client that is used to interact with all functions.

    Attributes:
        entrypoint_url (str): an entrypoint URL.
        proxy (Optional[dict[str, str]]): an HTTP or SOCKS5 IPv4 proxy dictionary.

    """
    __credentials: OKXCredentials
    entrypoint_url: str
    proxy: str | None = None

    def __init__(
            self, credentials: OKXCredentials, entrypoint_url: str = 'https://www.okx.com', proxy: str | None = None,
            check_proxy: bool = True
    ) -> None:
        """
        Initialize the class.

        Args:
            credentials (OKXCredentials): an instance with all OKX API key data.
            entrypoint_url (str): an API entrypoint url. (https://www.okx.com)
            proxy (Optional[str]): an HTTP or SOCKS5 IPv4 proxy in one of the following formats:

                - login:password@proxy:port
                - http://login:password@proxy:port
                - socks5://login:password@proxy:port
                - proxy:port
                - http://proxy:port

            check_proxy (bool): check if the proxy is working. (True)

        """
        self.__credentials = credentials
        self.entrypoint_url = entrypoint_url
        if proxy:
            try:
                if 'http' not in proxy and 'socks5' not in proxy:
                    proxy = f'http://{proxy}'

                if 'socks5' in proxy and 'socks5h' not in proxy:
                    proxy = proxy.replace('socks5', 'socks5h')

                self.proxy = proxy
                if check_proxy:
                    your_ip = requests.get(
                        'http://eth0.me/', proxies={'http': self.proxy, 'https': self.proxy}, timeout=10
                    ).text.rstrip()
                    if your_ip not in proxy:
                        raise InvalidProxy(f"Proxy doesn't work! Your IP is {your_ip}.")

            except InvalidProxy:
                pass

            except Exception as e:
                raise InvalidProxy(str(e))

        try:
            requests.get(self.entrypoint_url + '/api/v5/public/time', proxies={'http': self.proxy, 'https': self.proxy})

        except requests.exceptions.ConnectionError:
            self.entrypoint_url = 'https://www.okx.cab'
            requests.get(self.entrypoint_url + '/api/v5/public/time', proxies={'http': self.proxy, 'https': self.proxy})

        self.asset = Asset(credentials=self.__credentials, entrypoint_url=self.entrypoint_url, proxy=self.proxy)
        self.subaccount = Subaccount(
            credentials=self.__credentials, entrypoint_url=self.entrypoint_url, proxy=self.proxy
        )
