# Normal Imports

import requests
from requests import Request
import hmac

# Google OAuth2 Imports
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Miscellaneous Imports
# pip install numpy
# pip install pandas

from client import FtxClient
import numpy as np
import pandas as pd
import datetime
import time
import ftx
import json



class FTX_Client:
    api_endpoint = "https://ftx.com/api/markets" 
    def __init__(self, api_key = None, api_secret = None, subaccount_name = None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name
    

# Initializing FTX API requirements

# API_KEY = ""
# SECRET_KEY = ""

# GET /markets
# Gets data for all FTX markets

api_url = 'https://ftx.us/api'
markets_url = api_url + '/markets'
markets_response = requests.get(markets_url).json()
# print(markets)
data = markets_response['result']
markets_df = pd.DataFrame(data)
markets_df = markets_df.set_index('name')
# print(markets_df)

# GET /markets/{market_name}
# Gets data for single FTX market

market_name = 'ETH/USD'
market_path = f'/markets/{market_name}'
market_url = api_url + market_path
market_response = requests.get(market_url).json()
market_df = pd.DataFrame(market_response)['result']
# print(market_df)

# GET /markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}
# Gets historical market data

seconds_per_day = 60*60*24
start = datetime.datetime(2022,4,1).timestamp()
historical_path = f'/markets/{market_name}/candles?resolution={seconds_per_day}&start_time={start}'
historical_url = api_url + historical_path
historical_response = requests.get(historical_url).json()
historical_df = pd.DataFrame(historical_response['result'])
# print(historical_df)
historical_df['date'] = pd.to_datetime(historical_df['startTime'])
# print(historical_df)

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SERVICE_ACCOUNT_FILE = ('key.json')
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# spreadsheetURL = 'URL'
# service = build('sheets', 'v4', credentials=creds)