#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import time
# Creating Gemini websocket class
class Gemini_Websocket():

    def __init__(self, queue, socket, coins = []):
        self.queue = queue
        self.coins = coins
        self.socket = socket
        # self.sub_message = self.on_open()


    #generates a subscribe message to be converted into json to be sent to endpoint
    # def on_open(self):
    #     subscribe_message = {}
    #     subscribe_message["type"] = "subscribe"
    #     subscribe_message["subscriptions"] = [{"name":"l1", "symbols":self.coins}]
    #     return subscribe_message
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
        try:
            async with websockets.connect(self.socket) as websocket:
                # await websocket.send(json.dumps(self.sub_message))
                while True:
                    message = await websocket.recv()
                    self.queue.put(message)
                    if self.queue.full():
                        pass
                    print('Gemini Data Received')
                    print(message)
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(coins): 
    q = multiprocessing.Queue()
    socket = 'wss://api.gemini.com/v1/marketdata/BTCUSD'
    gws = Gemini_Websocket(q, socket, coins)
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["BTCUSD","ETHUSD","ETHBTC"]):
    asyncio.run(main(coins))
run()