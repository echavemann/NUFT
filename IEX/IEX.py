import pyEX as p
import pandas as pd

symbol = 'AAPL'
c = p.client(api_token='',version = 'sandbox')
chart = p.chart(symbol, timeframe='1m', date = None, token ='', version = '', filter='')
pd.DataFrame(c.batchDF(symbols=symbol, fields='chart', last=365, range_='1y')['chart'])
