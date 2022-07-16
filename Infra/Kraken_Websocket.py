#Dependencies
import asyncio
import websockets
import requests
import multiprocessing
import json

# Creating Kraken websocket class
class Kraken_Websocket():

    def __init__(self, queue, coins):
        self.queue = queue
        self.coins = coins
        self.socket = 'wss://ws.kraken.com/'

    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
        try:
            async with websockets.connect(self.socket) as websocket:
                await websocket.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
                while True:
                    message = await websocket.recv()
                    self.queue.put(message)
                    print('Kraken Data Received')
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(): 
    q = multiprocessing.Queue()
    cwr = Kraken_Websocket(q,[])
    await cwr.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run():
    asyncio.run(main())

run()