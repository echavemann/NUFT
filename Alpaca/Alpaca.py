from sys import api_version
import numpy as np
import pandas as pd
import scipy as sci
import alpaca_trade_api as tradeapi
import logging
import matplotlib as plt
import os

APCA_API_KEY_ID = 'key'
APCA_API_SECRET_KEY= 'secret'
APCA_API_BASE_URL = 'https://paper.api.alpaca.markets' 

api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL, api_version= 'v2')
account = api.get_account()

def marketorder (ticker, qty):
    qty = str(qty)
    if '$' in qty:
        qty = qty.remove('$')
        tradeapi.submit_order(
            symbol= ticker,
            notional = qty,
            side = 'buy',
            type = 'market',
            time_in_force = 'day',
        )
            
    else:
        tradeapi.submit_order(
            symbol = ticker,
            qty=qty,
            side='buy',
            type = 'market',
            time_in_force = 'day',
    )

def outpositions():
    portfolio = tradeapi.list_postions()
    for position in portfolio:
        print("{} shares of {}".format(position.qty,position.symbol))


