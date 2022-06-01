import requests,json 

from config import *
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "[]/v2/orders".format(BASE_URL)
HEADERS = {'APCA_API_KEY_ID': API_KEY, 'APCA_API_SECRET_KEY':SECRET_KEY}
#need to autheticate the API using the secret key and the api key 
def get_account():
    r = requests.get(ACCOUNT_URL, headers =  HEADERS)
    return json.loads(r.content)  #need to access the keys in the r.content dictionary 

#there are multiple endpoints 
#for the account one -> need to get the account associated with the api key 
    print(r.content) #returns a list of the the portfolio value, cash, multiplier..

#making reuquesting a new order

def create_order(symbol, qty, side, type, time_in_force):
    data =  {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json =data, headers = HEADERS)
    return json.loads(r.content)

#example code
new_order1=create_order("AAPL",100, "buy", "market","gtc")
print(new_order1)

#to see the list of orders 

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)

   
