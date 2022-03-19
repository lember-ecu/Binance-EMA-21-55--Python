from binance import Client
import pandas as pd
from ta.trend import ema_indicator

api_key = ""
secret_key = ""
client = Client(api_key, secret_key)
symbol = input("Symbol (like CHZUSDT):").upper()
intervalinput = input("Interval (1h, (30,15,5,3,1)m):").lower()
lookbackvalues = {"1h": "6000", "30m": "3000", "15m": "1500", "5m": "500", "3m": "300", "1m": "100"}

def getminutedata(symbol, interval, lookback):
    data = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC'))
    data = data.iloc[:,:6]
    data.columns = ["Time","Open","High","Low","Close","Volume"]
    data = data.set_index("Time")
    data.index = pd.to_datetime(data.index, unit="ms")
    data = data.astype(float)
    return data

df = getminutedata(symbol, intervalinput, lookbackvalues[intervalinput])

def applytechnicals(df):
    df["ema21"] = ema_indicator(df.Close, 21)
    df["ema55"] = ema_indicator(df.Close, 55)
    df.dropna(inplace = True)

applytechnicals(df)
print(df)
