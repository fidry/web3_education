class WrongChainID(Exception):
    pass


class WrongCoinSymbol(Exception):
    pass


class ClientException(Exception):
    pass


class InvalidProxy(ClientException):
    pass
