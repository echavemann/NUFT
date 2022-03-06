import requests
import yfinance as yf
from datetime import date
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

#Sheet cpmfog
url = "https://yfapi.net/v6/finance/quote"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

spreadsheetURL = 'URL'

service = build('sheets', 'v4', credentials=creds)

#Here we will have to fill in and/or import our ENTIRE watchlist.
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
#Spreadsheet logic in progress. 
today = ('1969-12-12')
#Y-M-D

#sheet logic - this tells it to compute a new one if the date has changed since the last minute. 
if today != date.today():
    new_sheet = {'requests': [
                {'addSheet':{'properties':{'title':date.today()}}}
    ]}
    today = date.today()
    res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetURL, body=new_sheet).execute()


