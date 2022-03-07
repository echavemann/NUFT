import requests
import yfinance as yf
import time
from pprint import pprint
from datetime import date
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
#i is counter for each day
i = 0

#Sheet comfig
url = "https://yfapi.net/v6/finance/quote"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
spreadsheetURL = 'URL'
service = build('sheets', 'v4', credentials=creds)

#Import from page one of the sheet.
watchlist = service.spreadsheets().values().get(spreadsheetId=spreadsheetURL, range = '!A').execute()
watchlist = watchlist['values']

#YF Overview
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

#loop value
today = ('1969-12-12')
#Y-M-D
while true:
    for stock in watchlist:
        tick = yf.Ticker(stock)
        stack = tick.info
    #store stack values
    #Test date
        if today != date.today():
            today = date.today()
            new_sheet = {'requests': [
                    {'addSheet':{'properties':{'title':date.today()}}}]}
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetURL, body=new_sheet).execute()     
        j = '!' + 'i'
        service.spreadsheets().values().update(spreadsheetId = spreadsheetURL, range = today + j, valueInputOption = 'USER_ENTERED', body = {stack}).execute()
        i+=1
        sleeptime = 60-datetime.utcnow().second
        time.sleep(sleeptime)

    
