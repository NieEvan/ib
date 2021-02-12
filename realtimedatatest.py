import asyncio
from ib_insync import IB, util
from ib_insync.contract import *
import pandas as pd

ib = IB()

ib.connect('127.0.0.1', 7497, clientId=1)

contract = Forex('EURUSD')

def onBarUpdate(bars, hasNewBar):
    df = util.df(bars)
    latest = df.tail(1)
    latest.to_csv('livedata.csv', mode='a', columns = ['time', 'open_' ,'high' , 'low', 'close'])
    data = pd.read_csv('livedata.csv')
    data = data.drop('Unnamed: 0', 1)
    # data = data.drop('endTime', 1)
    # data = data.drop('volume', 1)
    # data = data.drop('wap', 1)
    # data = data.drop('count', 1)

    print(data)


bars = ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)
bars.updateEvent += onBarUpdate

ib.sleep(23400) #开盘到收盘时间
ib.cancelRealTimeBars(bars)

# from ib_insync import *
# from IPython.display import display, clear_output
# # util.startLoop()

# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=1)

# contract = Stock('AAPL', 'SMART', 'USD')

# ib.reqHeadTimeStamp(contract, whatToShow='TRADES', useRTH=True)

# bars = ib.reqHistoricalData(
#         contract,
#         endDateTime='',
#         durationStr='1 D',
#         barSizeSetting='5 mins',
#         whatToShow='TRADES',
#         useRTH=True,
#         formatDate=1)

# df = util.df(bars)

# display(df.tail())
