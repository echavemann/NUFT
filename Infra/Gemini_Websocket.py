#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import time
# Creating Gemini websocket class
class Gemini_Websocket():

    def __init__(self, queue, coins):
        self.queue = queue
        self.coins = coins
        self.socket = "wss://api.gemini.com/v2/marketdata"
        self.sub_message = self.on_open()

    def on_open(self):
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["subscriptions"] = [{"name":"l2","symbols":["BTCUSD","ETHUSD","ETHBTC"]}]
        return subscribe_message
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
        try:
            async with websockets.connect(self.socket) as websocket:
                await websocket.send(json.dumps(self.sub_message))
                while True:
                    message = await websocket.recv()
                    self.queue.put(message)
                    print('Gemini Data Received')
                    print(message)
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(): 
    q = multiprocessing.Queue()
    gws = Gemini_Websocket(q,[])
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run():
    asyncio.run(main())

run()