import requests
import yfinance as yf
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

today = date.today()
watchlist = {}
#module
msft = yf.Ticker("MSFT")
msft.info #Open, H, L, C, Volume, Div, Splits, 
msft.history() #Args:
#Period - data to dl (1d)
#Interval (1m)
#start
#end
#prepost (Include pre and post: default to false)
#auto_adjust (adjusts, defaults to true)
#actions (bools dividends :)
#Process: For each stock in our dict, call info. Rate sort those into our sheets. Repeat. 
for stock in watchlist:
    tick = yf.Ticker(stock)
    stack = tick.info
    #store stack values
    
    








url = "https://yfapi.net/v6/finance/quote"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

spreadsheetURL = 'URL'

service = build('sheets', 'v4', credentials=creds)