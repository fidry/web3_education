from typing import Any


class WrongChainID(Exception):
    pass


class WrongCoinSymbol(Exception):
    pass


class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass


class TransactionException(Exception):
    pass


class GasPriceTooHigh(Exception):
    pass


class HTTPException(Exception):
    """
    An exception that occurs when an HTTP request is unsuccessful.

    Attributes:
        response (Optional[Dict[str, Any]]): a JSON response to a request.
        status_code (Optional[int]): a request status code.

    """
    response: dict[str, Any] | None
    status_code: int | None

    def __init__(self, response: dict[str, Any] | None = None, status_code: int | None = None) -> None:
        """
        Initialize the class.

        Args:
            response (Optional[Dict[str, Any]]): a JSON response to a request. (None)
            status_code (Optional[int]): a request status code. (None)

        """
        self.response = response
        self.status_code = status_code
