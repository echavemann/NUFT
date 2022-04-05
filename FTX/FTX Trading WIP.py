# Normal Imports

import requests
from requests import Request
import hmac

# Google OAuth2 Imports
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Miscellaneous Imports
# pip install numpy
# pip install pandas

import numpy as np
import pandas as pd
import datetime
import time
import ftx
import json

# Initializing FTX API requirements

api_url = 'https://ftx.us/api'
API_KEY = ""
SECRET_KEY = ""

# GET /account
# Gets account data

def get_account():
    ts = int(time.time() * 1000)
    account_url = api_url + '/account'
    request = Request('GET', account_url)
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(SECRET_KEY.encode(), signature_payload, 'sha256').hexdigest()

    prepared.headers['FTX-KEY'] = API_KEY
    prepared.headers['FTX-SIGN'] = signature
    prepared.headers['FTX-TS'] = str(ts)
    response = Request('GET', account_url, headers = prepared.headers)
    return response

def get_account_2():
    account_url = api_url + '/account'
    request = Request('GET', account_url)
    response = request.json()
    data = response['result']
    return data
print(get_account())
print(get_account_2)
# GET /markets
# Gets data for all FTX markets

def get_markets():
    markets_url = api_url + '/markets'
    markets_response = requests.get(markets_url).json()
    # print(markets)
    markets_data = markets_response['result']
    markets_df = pd.DataFrame(markets_data)
    markets_df = markets_df.set_index('name')
    return markets_df

# get_markets()

# GET /markets/{market_name}
# Gets data for single FTX market

def get_market(market_name):
    market_path = f'/markets/{market_name}'
    market_url = api_url + market_path
    market_response = requests.get(market_url).json()
    market_df = pd.DataFrame(market_response)['result']
    return market_df

# get_market('AAVE/USD')

# GET /markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}
# Gets historical market data

def get_hist(market_name):
    seconds_per_day = 60*60*24
    start = datetime.datetime(2022,4,1).timestamp()
    historical_path = f'/markets/{market_name}/candles?resolution={seconds_per_day}&start_time={start}'
    historical_url = api_url + historical_path
    historical_response = requests.get(historical_url).json()
    historical_df = pd.DataFrame(historical_response['result'])
    historical_df['date'] = pd.to_datetime(historical_df['startTime'])
    historical_df = historical_df.drop(columns=['startTime','time'])
    return historical_df

# GET /markets/{market_name}/orderbook?depth={depth}
# Gets orderbook data

def get_orderbook(market_name):
    orderbook_depth = 20
    orderbook_path = f'/markets/{market_name}/orderbook?depth={orderbook_depth}'
    orderbook_url = api_url + orderbook_path
    orderbook_response = requests.get(orderbook_url).json()

    # Prints orderbook asks and bids

    bids = pd.DataFrame(orderbook_response['result']['bids'])
    bids.columns = ['Bid Price','Bid Amount']

    # print(bids)

    asks = pd.DataFrame(orderbook_response['result']['bids'])
    asks.columns = ['Ask Price','Ask Amount']

    # print(asks)

    # Merge {bids} and {asks} to one DataFrame

    orderbook_df = pd.merge(bids,asks,left_index = True,right_index = True)
    return orderbook_df

### TESTS
# get_markets()
# print(get_market('ETH/USD'))
# print(get_hist('ETH/USD'))
# print(get_orderbook('ETH/USD'))



# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SERVICE_ACCOUNT_FILE = ('key.json')
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# spreadsheetURL = 'URL'
# service = build('sheets', 'v4', credentials=creds)
