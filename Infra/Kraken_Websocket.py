#Dependencies
import asyncio
import websockets
import multiprocessing
import json

# Creating Kraken websocket class
class kraken_websocket_raw():

    def __init__(self, queue, socket, ids = [], channels = []):
        self.queue = queue
        self.socket = socket
        self.ids = ids
        self.channels = channels
        self.sub_message = self.on_open()
    
    def on_open(self): # Generates a subscribe message to be converted into json to be sent to endpoint
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["product_ids"] = self.ids
        subscribe_message["channels"] = self.channels
        return subscribe_message
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
        try:
            async with websockets.connect(self.socket) as websocket:
                await websocket.send(json.dumps(self.sub_message))
                while True:
                    message = await websocket.recv()
                    self.queue.put(message)
                    print('Kraken Message Received')
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(): 
    q = multiprocessing.Queue()
    ids = ['BTC-USD','ETH-USD']
    channels = ["ticker"]
    socket = 'wss://ws.kraken.com/'
    kws = kraken_websocket_raw(q,socket,ids,channels)
    await kws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run():
    asyncio.run(main())
run()