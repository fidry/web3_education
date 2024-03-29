import base64
import hmac
import json
from datetime import datetime
from urllib.parse import urlencode

from aiohttp import TCPConnector
from aiohttp_socks import ProxyConnector

from libs.py_okx_async import exceptions
from libs.py_okx_async.models import OKXCredentials, Methods
from libs.py_okx_async.utils import async_get, async_post


class Base:
    """
    The base class for all section classes.

    Attributes:
        entrypoint_url (str): an entrypoint URL.
        proxy (str): an HTTP or SOCKS5 IPv4 proxy dictionary.
        connector (Optional[ProxyConnector]): a connector.

    """
    __credentials: OKXCredentials
    entrypoint_url: str
    proxy: str | None
    connector: ProxyConnector | TCPConnector = TCPConnector(force_close=True)

    def __init__(self, credentials: OKXCredentials, entrypoint_url: str, proxy: str | None) -> None:
        """
        Initialize the class.

        Args:
            credentials (OKXCredentials): an instance with all OKX API key data.
            entrypoint_url (str): an API entrypoint url.
            proxy (Optional[str]): an HTTP or SOCKS5 IPv4 proxy in one of the following formats:
                - login:password@proxy:port
                - http://login:password@proxy:port
                - socks5://login:password@proxy:port
                - proxy:port
                - http://proxy:port

        """
        self.__credentials = credentials
        self.entrypoint_url = entrypoint_url
        self.proxy = proxy
        if proxy:
            self.connector = ProxyConnector.from_url(
                url=proxy.replace('socks5h', 'socks5'), rdns=True, force_close=True
            )

    @staticmethod
    async def get_timestamp() -> str:
        """
        Get the current timestamp.

        Returns:
            str: the current timestamp.

        """
        return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    async def generate_sign(self, timestamp: str, method: str, request_path: str, body: dict | str) -> bytes:
        """
        Generate signed message.

        Args:
            timestamp (str): the current timestamp.
            method (str): the request method is either GET or POST.
            request_path (str): the path of requesting an endpoint.
            body (Union[dict, str]): POST request parameters.

        Returns:
            bytes: the signed message.

        """
        if not body:
            body = ''

        if isinstance(body, dict):
            body = json.dumps(body)

        key = bytes(self.__credentials.secret_key, encoding='utf-8')
        msg = bytes(timestamp + method + request_path + body, encoding='utf-8')
        return base64.b64encode(hmac.new(key, msg, digestmod='sha256').digest())

    async def make_request(
            self, method: str, request_path: str, body: dict | None = None
    ) -> dict[str, ...] | None:
        """
        Make a request to the OKX API.

        Args:
            method (str): the request method is either GET or POST.
            request_path (str): the path of requesting an endpoint.
            body (Optional[dict]): request parameters. (None)

        Returns:
            Optional[dict[str, ...]]: the request response.

        """
        timestamp = await self.get_timestamp()
        method = method.upper()
        body = body if body else {}
        if method == Methods.GET and body:
            request_path += f'?{urlencode(query=body)}'
            body = {}

        sign_msg = await self.generate_sign(timestamp=timestamp, method=method, request_path=request_path, body=body)
        url = self.entrypoint_url + request_path
        header = {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': self.__credentials.api_key,
            'OK-ACCESS-SIGN': sign_msg.decode(),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.__credentials.passphrase
        }
        if method == Methods.POST:
            response = await async_post(
                url=url, headers=header, connector=self.connector,
                data=json.dumps(body) if isinstance(body, dict) else body
            )

        else:
            response = await async_get(url=url, headers=header, connector=self.connector)

        if int(response.get('code')):
            raise exceptions.APIException(response=response)

        return response
