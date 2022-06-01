#Dependencies
import asyncio
import websockets
import multiprocessing
import json

#

class binance_websocket_raw():

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
            async with websockets.connect('wss://stream.binance.com:9443/ws') as websocket:
                await websocket.send(json.dumps(self.request))
                while True:
                        message = await websocket.recv()
                        self.queue.put(message)
                        print('Binance')
        except Exception:
            import traceback
            print(traceback.format_exc())
    
    def start(self):
        self.run()


async def main():
    q = multiprocessing.Queue()
    coins = ['BTCUSDT','ETHUSDT']
    bwr = binance_websocket_raw(q,coins=coins)
    # this example's getting market tickers for the specified coin types here, per the doc of binance, tickers come once every sec
    # if need sth else(like order book) just change generate_params's '@ticker' to whatever u want
    # or leave coins empty to get all market tickers
    await bwr.run()

#Non-async wrapper so MP can run it. 
def run():
    asyncio.run(main())