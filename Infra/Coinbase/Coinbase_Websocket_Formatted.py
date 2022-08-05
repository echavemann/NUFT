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
            async with websockets.connect(self.socket) as websocket:
                await websocket.send(json.dumps(self.sub_message))
                while True:
                    message = await websocket.recv()
                    temp_json = json.loads(message)
                    #Setting Variables for Data Frame 
                    msg_data = []
                    time_id = []
                    curr_dt = None 

                    if temp_json['type'] == 'message':
                        curr_dt = datetime.utcfromtimestamp(temp_json['T']/1000).strftime('%Y-%m-%d %H:%M:%S')
                        msg_data = {
                            'exchange': 'coinbase',
                            'ticker': temp_json['subject'],
                            'price': temp_json['data']['price'],
                        }
                        
                        time_id = [curr_dt]
                    
        
        
        
        
        
        # except Exception:
        #     import traceback
        #     print(traceback.format_exc())

        


    #goal is to get the DateTime from the Json and store into tickers 
    #then put into database 
