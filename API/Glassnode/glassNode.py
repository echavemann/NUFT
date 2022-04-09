import requests
import pandas as pd
import time
import numpy as np

# Instructions:
#
# from glassNode import getAPI
#
# getAPI(
#    symbol {string}, 
#    dataCat {string},
#    dataName {string}, 
#    APIKey [string, optional = ''],
#    currency [string, optional = False, use only applicable to data type]
#    interval [string, optional = "24h"],
#    time_end [int, optional = 0{years}, aka today],
#    time_start [optional = 1{years}],
# ) -> list of dates AND values(numpy.array), list of dates(numpy.array), list of values(numpy.array)
# 
# example: Illquid supply:
# link: https://api.glassnode.com/v1/metrics/supply/illiquid_sum
# dataCat = "supply"
# dataName = "illiquid_sum"

def getAPI(symbol, dataCat, dataName, APIKey = '', currency = False, interval = "24h", time_end = 0, time_start = 1):
    
    start_date = (time.time() - (time_start * 31536000))
    end_date = (time.time() - - (time_end * 31536000))

    if currency == False:
        data = requests.get('https://api.glassnode.com/v1/metrics/' + dataCat + '/' + dataName, 
            params = {
                'a': symbol,
                'api_key': APIKey,
                'i': interval,
                's':int(start_date),
                'u':int(end_date),
            },
        )
    else:
        data = requests.get('https://api.glassnode.com/v1/metrics/' + dataCat + '/' + dataName, 
            params = {
                'a': symbol,
                'api_key': APIKey,
                'i': interval,
                's':int(start_date),
                'u':int(end_date),
                'c':currency,
            },
        )
    
    if data.status_code != 200:  #lel try except doesnt work
        print("Unknown Request Error")
        return 1
    else:
        df = pd.read_json(data.text, convert_dates=['t'])

        date = np.asarray(df["t"])

        value = np.asarray(df.drop("t", inplace=True))

        df = np.asarray(df)

        return df, date, value