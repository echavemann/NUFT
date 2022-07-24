# #Dependencies
# import asyncio
# import websockets
# import multiprocessing
# import json
# import time
# # Creating Gemini websocket class
# class Gemini_Websocket():

#     def __init__(self, queue, socket, coins = []):
#         self.queue = queue
#         self.coins = coins
#         self.socket = socket
#         self.sub_message = self.on_open()


#     #generates a subscribe message to be converted into json to be sent to endpoint
#     def on_open(self):
#         subscribe_message = {}
#         subscribe_message["request"] = "/v1/order/events"
#         subscribe_message["nonce"] = time.time()
#         return subscribe_message
    
#     async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue
#         try:
#             async with websockets.connect(self.socket, max_size=1_000_000_000) as websocket:
#                 await websocket.send(json.dumps(self.sub_message))
#                 while True:
#                     message = await websocket.recv()
#                     self.queue.put(message)
#                     if self.queue.full():
#                         pass
#                     print('Gemini Data Received')
#                     print(message)
#         except Exception:
#             import traceback
#             print(traceback.format_exc())

#     def start(self):
#         self.run()
    
# async def main(coins): 
#     q = multiprocessing.Queue()
#     socket = 'wss://api.gemini.com/v1/multimarketdata?symbols=' + ','.join(coins) 
#     gws = Gemini_Websocket(q, socket, coins)
#     await gws.run()

# # Notice: Non-Async Wrapper is required for multiprocessing to run
# def run(coins = ["ETHUSD","ETHBTC"]):
#     asyncio.run(main(coins))
# run()

#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import time
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# Creating Gemini websocket class
class Gemini_Websocket():

    def __init__(self, queue, socket, coins = []):
        self.queue = queue
        self.coins = coins
        self.socket = socket
        self.sub_message = self.message_generator()

    #generates a subscribe message to be converted into json to be sent to endpoint for lvl 1 market data
    def on_openlvl1(self):
        subscribe_message = {}
        subscribe_message["request"] = "/v1/order/events"
        subscribe_message["nonce"] = time.time()
        return subscribe_message

    #generates a subscribe message to be converted into json to be sent to endpoint for lvl 2 market data
    def on_openlvl2(self):
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["subscriptions"] = [{"name":"l2","symbols":self.coins}]
        return subscribe_message

    def message_generator(self):
        if self.socket == 'wss://api.gemini.com/v2/marketdata':
            return self.on_openlvl2()
        else:
            return self.on_openlvl1()
        
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into either queue1 and queue2
        while True: #loop to keep websocket open since market 
            try:
                async with websockets.connect(self.socket, ping_interval=None, max_size=1_000_000_000) as websocket:
                    
                    await websocket.send(json.dumps(self.sub_message))

                    while True:
                        receive = await websocket.recv()

        
                        #convert response to json (apparently converting to json raises the 
                        #"asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes" and "websockets.exceptions.ConnectionClosedError: no close frame received or sent" error
                        #for market lvl 1 data websocket "gws1"
                        message = json.loads(receive)
                        
                        # print(message)
                        print('Gemini Data Received')
                        
                        # distinguish lvl 2 data from the message
                        if message.get("type") == "l2_updates":
                        # if self.socket == 'wss://api.gemini.com/v2/marketdata':
                            self.queue.put(message)
                            if self.queue.full():
                                pass
                            print('Level 2 Received')
                            print(message)

                        # distinguish lvl 1 data from the message
                        elif message.get("type") == "update":
                        # else:

                            self.queue.put(message)
                            if self.queue.full():
                                pass
                            # print(message)
                            print('Level 1 Received')

            except Exception:
                websocket = await websockets.connect(self.socket, ping_interval=None, max_size=1_000_000_000) #to reconnect "gws1" socket since it will disconnect every time with error code 1006
                import traceback
                print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(coins): 
    queue = multiprocessing.Queue()
    socket1 = 'wss://api.gemini.com/v1/multimarketdata?symbols=' + ','.join(coins) 
    socket2 = 'wss://api.gemini.com/v2/marketdata'
    gws1 = Gemini_Websocket(queue, socket1, coins)
    gws2 = Gemini_Websocket(queue, socket2, coins)
    await gws1.run()
    # await gws2.run()
    

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["ETHUSD","ETHBTC"]):
    asyncio.run(main(coins))

run()