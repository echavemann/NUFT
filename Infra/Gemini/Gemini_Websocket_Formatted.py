#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import pandas
import time
from datetime import datetime

# Creating Gemini websocket class
class Gemini_Websocket():

    def __init__(self, queue, socket, coins = []):
        self.queue = queue
        self.coins = coins
        self.socket = socket
        self.sub_message = self.on_open()
        # self.update_message = self.update_response()

    #generates a subscribe message to be converted into json to be sent to endpoint
    def on_open(self):
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["subscriptions"] = [{"name":"l2","symbols":self.coins}]
        return subscribe_message
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
        try:
            async with websockets.connect(self.socket) as websocket:
                await websocket.send(json.dumps(self.sub_message))
                # await websocket.send(json.dumps(self.update_message))  #Takes around 20 seconds for update messages to show up...
                while True:
                    ### 07/22/2022
                    ### Formatting Stuff Starts Here
                    # Receive Message
                    message = await websocket.recv()
                    #Convert message to json
                    temp_json = json.loads(message)
                    # Set variables that will be entered into DataFrame
                    msg_data = []
                    time_id = []
                    curr_dt = None

                    # if the request is of type l2_updates (message for lvl2 market data), get the DateTime from the json
                    if temp_json['type'] == 'l2_updates':
                        if 'trades' in temp_json.keys():
                        #check to see if timestamp is available to get
                            if "timestamp" in temp_json.get("trades")[0].keys():
                                curr_dt = datetime.fromtimestamp(time.time())  
                                # print(temp_json)
                                # curr_dt = datetime.utcfromtimestamp(temp_json.get("trades")[0].get("timestamp")/1000).strftime('%Y-%m-%d %H:%M:%S')
                                msg_data = {
                                    'exchange': 'gemini',
                                    'type': 'l2_updates',   
                                    'symbol': temp_json['symbol'],
                                    'action': temp_json['changes'][0][0],
                                    'price': temp_json['changes'][0][1],
                                    'quantity': temp_json['changes'][0][2]
                                }
                                # Prep index for DataFrame
                                time_id = [curr_dt]
                                

                    elif temp_json['type'] == 'trade':
                        curr_dt = datetime.utcfromtimestamp(temp_json["timestamp"]/1000).strftime('%Y-%m-%d %H:%M:%S')
                        # print(temp_json)
                        msg_data = {
                                'exchange': 'Gemini',
                                'type' : 'trade',
                                'symbol': temp_json['symbol'],
                                'action': temp_json['side'],
                                'price': temp_json['price'],
                                'quantity': temp_json['quantity']
                            }
                            # Prep index for DataFrame
                        time_id = [curr_dt]
                        print('GOGOGO')
                    if self.queue.full():
                        print("working")
                    
                    if msg_data != [] and time_id != []:
                        # Create DataFrame
                        df = pandas.DataFrame(data = msg_data, index=time_id)
                        print(df)
                        # put the dataframe into the queue
                        self.queue.put(df)
                
                        # self.queue.put(message)
                        # if self.queue.full():
                        #     pass
                        # print('Gemini Data Received')
                        # print(message)
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(coins): 
    q = multiprocessing.Queue()
    socket = 'wss://api.gemini.com/v2/marketdata'
    gws = Gemini_Websocket(q, socket, coins)
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["BTCUSD"]):
    asyncio.run(main(coins))
# run()