from typing import Optional


class OKXClientException(Exception):
    pass


class InvalidProxy(OKXClientException):
    pass


class APIException(OKXClientException):
    """
    An exception that occurs when the API is accessed unsuccessfully.

    Attributes:
        response (Optional[dict]): a JSON response to a request.
        status_code (Optional[int]): an HTTP status code.
        code (int): an OKX error code.
        msg (str): an OKX error message.

    Args:
        response (Optional[dict]): a JSON response to a request. (None)
        status_code (Optional[int]): an HTTP status code. (None)

    """
    response: Optional[dict]
    status_code: Optional[int]
    code: int
    msg: str

    def __init__(self, response: Optional[dict] = None, status_code: Optional[int] = None) -> None:
        self.response = response
        self.status_code = status_code
        try:
            self.code = int(self.response.get('code'))
            self.msg = self.response.get('msg')

        except:
            pass

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}, {self.msg}'

        return f'{self.status_code} (HTTP)'
