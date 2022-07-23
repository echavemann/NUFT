#Dependencies
import asyncio
import websockets
import multiprocessing
import json
import time
# Creating Gemini websocket class
class Gemini_Websocket():

    def __init__(self, queue1, queue2, socket1, socket2, coins = []):
        self.queue1 = queue1
        self.queue2 = queue2
        self.coins = coins
        self.socket1 = socket1
        self.socket2 = socket2
        self.sub_message1 = self.on_openlvl1()
        self.sub_message2 = self.on_openlvl2()
        self.update_message = self.update_response()

    #generates a subscribe message to be converted into json to be sent to endpoint
    def on_openlvl1(self):
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["subscriptions"] = [{"name":"l1","symbols":self.coins}]
        return subscribe_message

    def on_openlvl2(self):
        subscribe_message = {}
        subscribe_message["type"] = "subscribe"
        subscribe_message["subscriptions"] = [{"name":"l2","symbols":self.coins}]
        return subscribe_message

    #sent to endpoint for updating level 2 data response
    def update_response(self):
        subscribe_message = {}
        subscribe_message["type"] = "l2_updates"
        subscribe_message["subscriptions"] = [{"symbols":self.coins}]
        return subscribe_message
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue2
        try:
            async with websockets.connect(self.socket2) as websocket:
                await websocket.send(json.dumps(self.sub_message2))
                await websocket.send(json.dumps(self.update_message))  #Takes around 20 seconds for update messages to show up...
                while True:
                    message = await websocket.recv()

                    self.queue2.put(message)
                    if self.queue2.full():
                        pass
                    print('Gemini Data Received')
                    print(message)
        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(coins): 
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    socket1 = 'wss://api.gemini.com/v1/marketdata'
    socket2 = 'wss://api.gemini.com/v2/marketdata'
    gws = Gemini_Websocket(q1, q2, socket1, socket2, coins)
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["BTCUSD","ETHUSD","ETHBTC"]):
    asyncio.run(main(coins))

run()