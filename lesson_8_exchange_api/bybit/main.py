from bybit.bybit_api import Bybit
from bybit.models import Side, InstrumentInfo

from data import config


if __name__ == '__main__':
    ticker = 'ACAUSDT'

    bb = Bybit(config.bybit_credentials)
    print(bb.get_balance())
    print(bb.get_balance(coin='USDT'))

    print(bb.get_orderbook(symbol=ticker))

    instruments: list[InstrumentInfo] = bb.get_instruments(symbol=ticker)
    for instrument in instruments:
        print(instrument)

    instruments: list[InstrumentInfo] = bb.get_instruments(symbol='BTCUSDT')
    for instrument in instruments:
        print(instrument)

    print(bb.get_best_price(symbol='BTCUSDT', liquidity=25000, limit=50))

    print(bb.create_order(
        coin='USDT',
        symbol=ticker,
        side=Side.buy,
        qty=9.1234567,
        price=0.01
    ))

    # qty должен соответствовать base_precision
    # price должен соответствовать tick_size

    instrument_info = bb.get_instrument(symbol=ticker)

    print(bb.create_order(
        coin='ACA',
        symbol=ticker,
        side=Side.sell,
        # instrument_info=instrument_info
    ))

    bb.cancel_orders(symbol=ticker)

    print(bb.create_order(
        coin='ACA',
        symbol=ticker,
        side=Side.sell,
        qty=10.798687678678677,
        price=0.13832132142
    ))

    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.1'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.01'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.001'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.0001'))
