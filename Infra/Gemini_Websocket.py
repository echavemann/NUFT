#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import pandas
import time
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

    # #sent to endpoint for updating level 2 data response
    # def update_response(self):
    #     subscribe_message = {}
    #     subscribe_message["type"] = "l2_updates"
    #     subscribe_message["subscriptions"] = [{"symbols":self.coins}]
    #     return subscribe_message
    
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
                    curr_dt = []
                    
                    # if the request is of type l2_updates, get the DateTime from the json
                    # if temp_json['type'] == 'l2_updates':
                        # curr_dt = temp_json['data']['timestamp']

                        # # for each coin, get the data and append to msg_data
                        # for coin in self.coins:
                        #     msg_data.append(temp_json['data']['level2'][coin])
                        #     time_id.append(curr_dt)
                        # # create a dataframe from the msg_data and time_id
                        # df = pd.DataFrame(msg_data, columns=['bid', 'ask', 'last', 'volume', 'timestamp'], index=time_id)
                        # # put the dataframe into the queue
                        # self.queue.put(df)
            
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
    socket = 'wss://api.gemini.com/v2/marketdata'
    gws = Gemini_Websocket(q, socket, coins)
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["BTCUSD","ETHUSD","ETHBTC"]):
    asyncio.run(main(coins))
run()