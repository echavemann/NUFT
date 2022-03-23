from sys import api_version
import numpy as np
import pandas as pd
import scipy as sci
import alpaca_trade_api as tradeapi
import logging
import matplotlib as plt
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import oauth


APCA_API_KEY_ID = 'key'
APCA_API_SECRET_KEY= 'secret'
APCA_API_BASE_URL = 'https://paper.api.alpaca.markets' 

api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL, api_version= 'v2')
account = api.get_account()

def marketorder (ticker, qty,side):
    qty = str(qty)
    if '$' in qty:
        qty = qty.remove('$')
        tradeapi.submit_order(
            symbol= ticker,
            notional = qty,
            side = side,
            type = 'market',
            time_in_force = 'day',
        )
            
    else:
        tradeapi.submit_order(
            symbol = ticker,
            qty=qty,
            side=side,
            type = 'market',
            time_in_force = 'day',
    )

def outpositions():
    portfolio = tradeapi.list_postions()
    for position in portfolio:
        print("{} shares of {}".format(position.qty,position.symbol))

#Google Setup Stuff


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
spreadsheetURL = 'URL'
service = build('sheets', 'v4', credentials=creds)

