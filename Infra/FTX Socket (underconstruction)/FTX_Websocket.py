import datetime
import requests
import pandas as pd
import websockets
import json
import multiprocessing
import asyncio
# from FTXClient import FtxWebsocketClient
api_key = ''
api_secret = ''

#FTX market API

api_url = 'https://ftx.us/api'
api = '/markets'
url = api_url + api
print(url)

def get_markets():
    markets = requests.get(url).json()
    data = markets['result']
    print(data)
    df = pd.DataFrame(data)
    df = df.set_index('name')
    df.iloc[:,:4].head()

#this apparently gets all market data... you need to kill the script after a few seconds for the data to appear in the terminal
while True:
    get_markets()



# GET /markets/{market_name}
market_name = 'ETH/USD'
path = f'/markets/{market_name}'
url = api_url + path
url

res = requests.get(url).json()
df = pd.DataFrame(res)['result']
df

#trying to use binance as a model?

class FTX_websocket_raw():

    def __init__(self,queue,coins = []):
        self.queue = queue
        self.coins = coins
        self.params = self.generate_params(coins)
        self.request = self.generate_request()

    def generate_params(self,coins): # the params will be used to generate the request
        if coins == []:
            # get all market tickers if no coin is specified
            return '!ticker@arr'
        params = []
        for coin in coins:
            params.append(coin.lower()+'@trade')
        return params

    def generate_request(self): # request will be converted to a json and sent to the endpoint
        request = {}
        params = []
        for param in self.params:
            params.append(param)
        request["method"] = "SUBSCRIBE"
        request["params"] = params
        request["id"] = 1 # idk what this is but whatever positive integer works here
        return request

    async def run(self): # poweroverwhelming
        try:
            async with websockets.connect('wss://ftx.com/ws/') as websocket:
                await websocket.send(json.dumps(self.request))
                while True:
                        message = await websocket.recv()
                        self.queue.put(message)
                        print('FTX')
        except Exception:
            import traceback
            print(traceback.format_exc())
    
    def start(self):
        self.run()


# async def main():
#     q = multiprocessing.Queue()
#     coins = ['BTCUSDT','ETHUSDT']
#     fwr = FTX_websocket_raw(q,coins=coins)
#     # this example's getting market tickers for the specified coin types here, per the doc of binance, tickers come once every sec
#     # if need sth else(like order book) just change generate_params's '@ticker' to whatever u want
#     # or leave coins empty to get all market tickers
#     await fwr.run()

# #Non-async wrapper so MP can run it. 
# def run():
#     asyncio.run(main())




"""
HEADINGS
// Event type
// Event time
// Symbol
// Aggregate trade ID
// Price
// Quantity
// First trade ID
// Last trade ID
// Trade time
// Is the buyer the market maker?
// Ignore
"""