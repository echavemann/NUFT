from kucoin.client import Client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

#EnvironmentalVari
def get_spread_sheet_id():
	return ""
#Starts the kucoin client with supplied APIs (Stored in the google drive). 
def get_kucoin_client():
	api_key = ""
	api_secret = ""
	api_passphrase = ""
	client = Client(api_key, api_secret, api_passphrase)
	return client

#Wrapper for the API call with a certain client.
def get_ticker(client):
	ticker = client.get_ticker()
	return ticker

#Converts the ticker get from client to a list of list that 
#the googlesheets api can write into the given sheet
def ticker_to_list(ticker): 
	data = list(ticker.items())[1][1] 
	data_list = []
	for item in data:
		data_list.append(list(item.values()))
	return data_list

#Generates headings for Sheets
def ticker_headings(ticker):
	data = list(ticker.items())[1][1]
	return [list(data[0].keys())]


def write_ticker_data(client, service, sheetID): # writes the ticker ID into the sheet
	v = ticker_to_list(get_ticker(client))
	body = {"values":v}
	request = service.spreadsheets().values().update(
	spreadsheetId=sheetID, 
	range = "Kucoin!A2", 
	valueInputOption="USER_ENTERED", 
	body=body
	).execute()

  
def write_ticker_headings(client, service, sheetID): # writes the headings into the sheet
	v = ticker_headings(get_ticker(client))
	body = {"values":v}
	request = service.spreadsheets().values().update(
	spreadsheetId=sheetID, 
	range = "Kucoin!A1", 
	valueInputOption="USER_ENTERED", 
	body=body
	).execute()

  
def main(): 
	# gets data from kucoin api and then write it to the specified google sheet
  
  #GSheets Boiler
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	SERVICE_ACCOUNT_FILE = ('key.json')
	creds = None
	creds = service_account.Credentials.from_service_account_file(
		SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	service = build('sheets', 'v4', credentials=creds)
  #Using Helpers to construct KCoin
	spreadsheet_id = get_spread_sheet_id()
	client = get_kucoin_client()
  #Writing data with helpers.
	write_ticker_headings(client, service, spreadsheet_id) # this doesn't need to be executed everytime
	while True:
		write_ticker_data(client, service, spreadsheet_id)
		time.sleep(30)
		
main()
