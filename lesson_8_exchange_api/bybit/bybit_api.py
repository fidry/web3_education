from typing import Optional

from pybit.unified_trading import HTTP

from models import (
    ByBitCredentials,
    Category,
    Side,
    OrderType,
    AccountType,
    InstrumentInfo,
    TimeInForce,
)

from data import config


'''
bybit documentation: https://bybit-exchange.github.io/docs/v5/intro
pybit documentation: https://pypi.org/project/pybit/
fix "no module Crypto" error: https://stackoverflow.com/questions/51824628/modulenotfounderror-no-module-named-crypto-error
'''


class Bybit:
    def __init__(
            self,
            credentials: ByBitCredentials,
            category: str = Category.spot,
            account_type: str = AccountType.spot
    ):
        if not credentials.completely_filled():
            raise Exception('Credentials are not filled in completely')

        self.category = category
        self.account_type = account_type

        self.session = HTTP(
            testnet=False,
            api_key=credentials.api_key,
            api_secret=credentials.api_secret
        )

    def get_balance(self, coin: Optional[str] = None) -> dict:
        coin_balance_dict = {}
        balances_lst = self.session.get_wallet_balance(accountType=self.account_type, coin=coin)['result']['list']
        for elem in balances_lst:
            for coin in elem['coin']:
                symbol = coin['coin']
                coin_balance = coin['free']
                coin_balance_dict[symbol] = coin_balance
        return coin_balance_dict

    def get_orderbook(self, symbol: str, limit: int = 3) -> dict:
        response = self.session.get_orderbook(category=self.category, symbol=symbol, limit=limit)
        orderbook_dict = response.get('result')
        if not orderbook_dict:
            raise Exception(f'Can not get orderbook ({response})')
        result_dict = {
            'asks': [],
            'bids': [],
        }
        for ask, bid in zip(orderbook_dict['a'], orderbook_dict['b']):
            result_dict['asks'].append(
                {'price': float(ask[0]), 'volume': float(ask[1])}
            )
            result_dict['bids'].append(
                {'price': float(bid[0]), 'volume': float(bid[1])}
            )
        return result_dict

    def get_instruments(self, symbol: Optional[str] = None) -> list[InstrumentInfo]:
        response = self.session.get_instruments_info(category=self.category, symbol=symbol)
        if not response:
            raise Exception(f'Can not get instrument info {response}')

        result_lst = []
        instruments = response.get('result', {}).get('list')
        for info in instruments:
            result_lst.append(InstrumentInfo(
                symbol=info.get('symbol'),
                base_coin=info.get('baseCoin'),
                base_precision=info.get('lotSizeFilter', {}).get('basePrecision'),
                quote_coin=info.get('quoteCoin'),
                quote_precision=info.get('lotSizeFilter', {}).get('quotePrecision'),
                min_order_qty=info.get('lotSizeFilter', {}).get('minOrderQty'),
                max_order_qty=info.get('lotSizeFilter', {}).get('maxOrderQty'),
                min_order_amt=info.get('lotSizeFilter', {}).get('minOrderAmt'),
                max_order_amt=info.get('lotSizeFilter', {}).get('maxOrderAmt'),
                tick_size=info.get('priceFilter', {}).get('tickSize'),
                status=info.get('status'),
            ))
        return result_lst

    def get_instrument(self, symbol: str) -> Optional[InstrumentInfo]:
        instruments = self.get_instruments(symbol=symbol)
        if instruments:
            return instruments[0]
        return None

    def get_best_price(self, symbol: str, liquidity: float, side: str = Side.buy, limit: int = 20):
        if not isinstance(liquidity, float):
            liquidity = float(liquidity)

        orderbook_liquidity = 0
        if side == Side.buy:
            prices = self.get_orderbook(symbol=symbol, limit=limit)['asks']
        else:
            prices = self.get_orderbook(symbol=symbol, limit=limit)['bids']

        for price_volume_dict in prices:
            orderbook_liquidity += price_volume_dict['price'] * price_volume_dict['volume']
            if orderbook_liquidity >= liquidity:
                return price_volume_dict['price']
        raise Exception(f'Can not sell/buy {liquidity} worth of {symbol}')

    def create_order(
            self,
            coin: str,
            symbol: str,
            side: str,
            qty: Optional[float] = None,
            order_type: str = OrderType.limit,
            price: Optional[float] = None,
            time_in_force: str = TimeInForce.GTC,
            check_symbol: bool = True,
            check_qty_and_price: bool = True,
            instrument_info: Optional[InstrumentInfo] = None
    ):
        '''
        https://bybit-exchange.github.io/docs/v5/order/create-order
        https://www.bybit.com/ru-RU/help-center/s/article/What-Are-Time-In-Force-TIF-GTC-IOC-FOK
        '''

        if check_symbol and not self.get_instrument(symbol=symbol):
            raise Exception(f'Can not get symbol: {symbol}')

        if not qty:
            qty = self.get_balance(coin=coin).get(coin)
            if not qty:
                raise Exception(f'Zero balance: {coin}')

        if order_type != OrderType.market and not price:
            price = self.get_best_price(symbol=symbol, liquidity=qty, side=side)

        if check_qty_and_price:
            qty, price = self.get_correct_qty_and_price(
                symbol=symbol, qty=qty, price=price, instrument_info=instrument_info)

        print(qty, price)

        return self.session.place_order(
            category=self.category,
            symbol=symbol,
            side=side,
            orderType=order_type,
            qty=qty,
            price=price,
            timeInForce=time_in_force
        )

    def cancel_orders(self, symbol: Optional[str] = None):
        response = self.session.get_open_orders(
            category=self.category,
            symbol=symbol,
        )
        orders = response.get('result', {}).get('list')
        for order in orders:
            print(order)

            if order["orderStatus"] == "New":
                self.session.cancel_order(
                    category=self.category,
                    symbol=symbol,
                    orderId=order['orderId'],
                    orderLinkId=order['orderLinkId'],
                )

    # @staticmethod
    # def round_to_accuracy(number, accuracy) -> tuple[str]:
    #     return round(number / accuracy) * accuracy

    @staticmethod
    def round_to_accuracy(number, accuracy) -> str:
        try:
            decimals = len(accuracy.split('.')[1])
            splited_number = str(number).split('.')
            return splited_number[0] + '.' + splited_number[1][:decimals]
        except IndexError:
            return number

    def get_correct_qty_and_price(
            self,
            symbol: str,
            qty: float,
            price: Optional[float],
            instrument_info: Optional[InstrumentInfo] = None
    ) -> tuple[Optional[str]]:
        # qty должен соответствовать base_precision, и количество должно быть больше min_order_qty
        # price должен соответствовать tick_size

        if not instrument_info:
            instrument_info = self.get_instrument(symbol=symbol)

        qty = Bybit.round_to_accuracy(qty, instrument_info.base_precision)

        if price:
            price = Bybit.round_to_accuracy(price, instrument_info.tick_size)

        return qty, price
