from bybit.bybit_api import Bybit
from bybit.models import Side, InstrumentInfo

from data import config


if __name__ == '__main__':
    bb = Bybit(config.bybit_credentials)
    print(bb.get_balance())
    print(bb.get_balance(coin='USDT'))

    print(bb.get_orderbook(symbol='DFIUSDT'))

    instruments: list[InstrumentInfo] = bb.get_instruments(symbol='DFIUSDT')
    for instrument in instruments:
        print(instrument)

    instruments: list[InstrumentInfo] = bb.get_instruments(symbol='BTCUSDT')
    for instrument in instruments:
        print(instrument)

    print(bb.get_best_price(symbol='BTCUSDT', liquidity=250000, limit=50))

    print(bb.create_order(
        coin='USDT',
        symbol='DFIUSDT',
        side=Side.buy,
        qty=4.1234567,
    ))

    # qty должен соответствовать base_precision
    # price должен соответствовать tick_size

    instrument_info = bb.get_instrument(symbol='DFIUSDT')

    print(bb.create_order(
        coin='DFI',
        symbol='DFIUSDT',
        side=Side.sell,
        # instrument_info=instrument_info
    ))

    bb.cancel_orders(symbol='DFIUSDT')

    print(bb.create_order(
        coin='DFI',
        symbol='DFIUSDT',
        side=Side.sell,
        qty=3.798687678678677,
        price=0.29832132142
    ))

    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.1'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.01'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.001'))
    print(Bybit.round_to_accuracy(number=1.234567, accuracy='0.0001'))

