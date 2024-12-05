'''
https://bybit-exchange.github.io/docs/v5/enum#category
'''

from dataclasses import dataclass


@dataclass
class ByBitCredentials:
    api_key: str
    api_secret: str

    def completely_filled(self) -> bool:
        return all((self.api_key, self.api_secret))


class Category:
    spot: str = 'spot'
    linear: str = 'linear'
    inverse: str = 'inverse'
    option: str = 'option'


class Side:
    buy: str = 'Buy'
    sell: str = 'Sell'


class OrderType:
    market: str = 'Market'
    limit: str = 'Limit'


# https://bybit-exchange.github.io/docs/v5/enum#accounttype
class AccountType:
    unified: str = 'UNIFIED'
    fund: str = 'FUND'


class TimeInForce:
    GTC: str = 'GTC'
    IOC: str = 'IOC'
    FOK: str = 'FOK'


@dataclass
class InstrumentInfo:
    symbol: str
    base_coin: str
    base_precision: str
    quote_coin: str
    quote_precision: str
    min_order_qty: str
    max_order_qty: str
    min_order_amt: str
    max_order_amt: str
    tick_size: str
    status: str

    def __str__(self):
        return f'{self.symbol}: (status: {self.status}; base_precision: {self.base_precision}; ' \
               f'quote_precision: {self.quote_precision}; min_order_qty: {self.min_order_qty}; ' \
               f'max_order_qty: {self.max_order_qty}; min_order_amt: {self.min_order_amt}; ' \
               f'max_order_amt: {self.max_order_amt}; tick_size: {self.tick_size})'
