import asyncio
import websockets
import requests
import multiprocessing
import time
import json
import pandas as pd
import traceback
from time import time
from datetime import datetime 
from scipy.fft import idst 
from uuid import uuid4

#https://docs.cloud.coinbase.com/exchange/docs/websocket-channels
#Creating Coinbase Websocket Class 
class Coinbase_Websocket():
    #Passing queue and other relevant information
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
    
    async def run(self): #Full Asynchronous Run 
        try:
            async with websockets.connect(self.socket) as websocket:
                await websocket.send(json.dumps(self.sub_message))
                while True:
                    message = await websocket.recv()
                    # print(message)
                    temp_json = json.loads(message)
                    #Setting Variables for Data Frame 
                    msg_data = []
                    time_id = []
                    curr_dt = None 
                    if temp_json['type'] == 'ticker':
                        curr_dt = temp_json['time'].replace('Z', '')
                        curr_dt = curr_dt.replace('T', ' ')
                        msg_data = {
                            'exchange': 'coinbase',
                            'ticker': temp_json['product_id'],
                            'price': temp_json['price']
                        }
                        time_id = [curr_dt]
                    if self.queue.full():
                        print('working')
                    if msg_data != [] and time_id != []:
                        df = pd.DataFrame(data = msg_data, index = time_id)
                        # print(df)
                        self.queue.put(df) 
                    if temp_json['type'] == 'l2update':
                        print(temp_json)
        except Exception:
            import traceback
            print(traceback.format_exc())

        

    #goal is to get the DateTime from the Json and store into tickers 
    #then put into database 
#Async Script Start
async def main(coins): 
    q = multiprocessing.Queue()
    channels = ['ticker', 'level2_batch']
    socket = 'wss://ws-feed.exchange.coinbase.com'
    cwr = Coinbase_Websocket(q,socket,coins,channels)
    await cwr.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ['BTC-USD','ETH-USD']):
    asyncio.run(main(coins))
run()