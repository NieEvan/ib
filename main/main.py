import time

from ib_insync import IB, BarDataList
from ib_insync.contract import *

from src.db import *
from src.project_config_util import get_yaml_logger

logger = get_yaml_logger("data")


def on_bar_update(bars: BarDataList, has_new_bar: bool):
    try:
        logger.debug("on_bar_update: {} {} {}".format(bars.contract, bars[-1], has_new_bar))
        df = util.df([bars[-1]])
        contract = bars.contract
        symbol = None
        if type(contract) == Forex:
            symbol = contract.symbol + contract.currency
        elif type(contract) == Stock:
            symbol = contract.symbol + contract.currency

        if has_new_bar and symbol:
            df['symbol'] = symbol
            update_k_bars(df=df, _type=bars.barSizeSetting)
    except Exception as e:
        logger.exception(e)


def test_request_realtime_bars(ib: IB):
    contract = Forex('EURUSD')
    bars = ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)
    bars.updateEvent += on_bar_update

    ib.sleep(100000)  # 开盘到收盘时间
    ib.cancelRealTimeBars(bars)
    return bars


def test_request_historical_data(ib: IB, contract: Contract, barSizeSetting: str):
    contract = Forex('EURUSD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='10 secs',
        # whatToShow='ADJUSTED_LAST',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1,
        keepUpToDate=True,
    )
    bars.updateEvent += on_bar_update
    return bars


def request_historical_data(ib: IB, contract: Contract, barSizeSetting: str):
    """
    订阅历史 K 线
    :param ib: ib_insync.IB 实例
    :param contract: 标的
    :param barSizeSetting: K 线类型, 参见 https://interactivebrokers.github.io/tws-api/historical_bars.html 的 Valid Bar Sizes
    :return: BarDataList
    """
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting=barSizeSetting,
        # whatToShow='ADJUSTED_LAST',
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1,
        keepUpToDate=True,
    )
    return bars


if __name__ == '__main__':
    # 创建 IB 对象并尝试连接
    try:
        ib = IB()
        ib.connect('127.0.0.1', 7497, clientId=2)

        contracts = [
            Forex('EURUSD'),
            Stock(symbol="AAPL", exchange="SMART", currency="USD"),
            Stock(symbol="1810", exchange="SEHK", currency="HKD"),
            Stock(symbol="601636", exchange="SEHKNTL"),
            Stock(symbol="000725", exchange="SEHKSZSE"),
        ]
        # 创建保存 K 线所用的 DB 表格
        create_tables()
        # 订阅 5 分钟 K 线
        for contract in contracts:
            try:
                bars = request_historical_data(ib=ib, contract=contract, barSizeSetting="5 mins")
                bars.updateEvent += on_bar_update
            except Exception as e1:
                logger.exception(e1)
        while True:
            time.sleep(100)
        # ib.sleep(1000)
    except Exception as e:
        logger.exception(e)
