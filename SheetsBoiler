from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import 

//Here's the pip for this!
//  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
spreadsheetURL = 'URL'
service = build('sheets', 'v4', credentials=creds)
