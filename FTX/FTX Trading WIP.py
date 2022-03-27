from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import numpy as np
import pandas as pd
import datetime
import time
from ftxapi import client
import json


# Here's the pip for this!
#   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

endpoint = "https://ftx.com/api/markets"
API_KEY = ""
SECRET_KEY = ""

all_markets = requests.get(endpoint_url).json()
df = pd.DataFrame(all_markets['result'])
df.set_index('name', inplace = True)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
spreadsheetURL = 'URL'
service = build('sheets', 'v4', credentials=creds)
