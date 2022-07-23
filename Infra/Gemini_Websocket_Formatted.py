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
    
    async def run(self): #on_message, sends json subscription to endpoint and awaits response to be put into queue1 and queue2
        try:
            async with websockets.connect(self.socket2) as websocket:
                await websocket.send(json.dumps(self.sub_message1))
                await websocket.send(json.dumps(self.sub_message2))
                while True:
                    payload = await websocket.recv()
                    message = json.loads(payload)

                    if message.get("type") == "l2_updates":
                        self.queue2.put(message)
                        if self.queue2.full():
                            pass
                        print('Level 2 Received')
                        print(message)

                    else:
                        self.queue1.put(message)
                        if self.queue1.full():
                            pass
                        print(message)
                        print('Level 1 Received')

        except Exception:
            import traceback
            print(traceback.format_exc())

    def start(self):
        self.run()
    
async def main(coins): 
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    socket1 = 'wss://api.gemini.com/v1/multimarketdata?symbols=' + ','.join(coins) 
    socket2 = 'wss://api.gemini.com/v2/marketdata'
    gws = Gemini_Websocket(q1, q2, socket1, socket2, coins)
    await gws.run()

# Notice: Non-Async Wrapper is required for multiprocessing to run
def run(coins = ["ETHUSD","ETHBTC"]):
    asyncio.run(main(coins))

run()