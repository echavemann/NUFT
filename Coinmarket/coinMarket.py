import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

headers = {
    'X-CMC_PRO_API_KEY' : 'e7a3971f-2c4f-4e03-bb13-5400dcded14c',
    'Accepts' : 'Application/json'
}

params = {
    'start': '1',
    'limit': '50',
    'convert' : 'USD'
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

paChong = requests.get(url, params = params, headers = headers).json()
coins = paChong['data']

for x in coins:
    print(x['symbol'], x['quote']['USD']['price'])

#print(returnValue)
