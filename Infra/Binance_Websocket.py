#Dependencies
import asyncio
import websockets
import multiprocessing
import json


#Build Websocket Class
class Binance_Websocket():

    def __init__(self,queue,coins = []):
        self.queue = queue
        self.coins = coins
        self.params = self.generate_params(coins)
        self.request = self.generate_request()

    def generate_params(self,coins): #Generate request paramaters
        if coins == []:
            # get all market tickers if no coin is specified
            return '!ticker@arr'
        params = []
        for coin in coins:
            params.append(coin.lower()+'@trade')
        return params

    def generate_request(self): #Send subscribe request to the endpoint.
        request = {}
        params = []
        for param in self.params:
            params.append(param)
        request["method"] = "SUBSCRIBE"
        request["params"] = params
        request["id"] = 1 #Internal ID, not used by us at this point. 
        return request

    async def run(self): #Full asynchronous run. 
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
    
    #Non-Async Wrapper
    def start(self):
        self.run()

#Async Script Start
async def main(coins):
    q = multiprocessing.Queue()
    bwr = Binance_Websocket(q,coins=coins)
    # this example's getting market tickers for the specified coin types here, per the doc of binance, tickers come once every sec
    # if need sth else(like order book) just change generate_params's '@ticker' to whatever u want
    # or leave coins empty to get all market tickers
    await bwr.run()

#Non-async wrapper so MP can run it. 
def run(coins = ['BTCUSDT','ETHUSDT']):
    asyncio.run(main(coins))

run()