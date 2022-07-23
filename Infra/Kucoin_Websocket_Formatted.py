import asyncio
from time import time 
import websockets
import requests
import multiprocessing
import time
import json
from datetime import datetime
from uuid import uuid4
import pandas as pd

level_two_list = []

class kucoin_websocket_raw():

    def __init__(self, queue_1, queue_2, topics = []):
        self.token = ''
        self.queue_1 = queue_1
        self.queue_2 = queue_2
        self.endpoint = ''
        self.connectid = ''
        self.wsendpoint = ''
        self.timeout = 0
        self.topics = topics
        self.last_ping = time.time()

    #prereq function
    def get_ws(self):
        r = requests.post('https://api.kucoin.com/api/v1/bullet-public')
        r = r.json()
        self.token = r['data']['token']
        self.endpoint = r['data']['instanceServers'][0]['endpoint']
        self.timeout = int(r['data']['instanceServers'][0]['pingTimeout'] / 1000) - 2
        self.connectid = str(uuid4()).replace('-', '')
        wsendpoint = f"{self.endpoint}?token={self.token}&connectId={self.connectid}"
        self.wsendpoint = wsendpoint
        
    #prereq function 2
    async def get_id(self):
        async with websockets.connect(self.wsendpoint) as websocket:
            message = await websocket.recv()
            self.connectid = message.split(',')[0].split(':')[1].replace('"', '')
            await websocket.close()
            
    #woooo
    async def _run(self):
        try:
            async with websockets.connect(self.wsendpoint, ping_interval=self.timeout, ping_timeout=None) as websocket:
                for topic in self.topics:
                    await websocket.send(json.dumps({
                        "id": self.connectid,
                        "type": 'subscribe',
                        "topic": topic,
                        "response": True
                    }))
                i = 0
                while i < 10:
                    ### 07/22/2022 
                    ### Formatting Stuff Starts Here
                    # Receive Message
                    message = await websocket.recv()
                    # Translate type str to json
                    temp_json = json.loads(message)
                    # Set variables that will be entered into DataFrame
                    msg_data = []
                    time_id = []
                    # If the request is a message, get the DateTime from the json
                    # if temp_json['topic']
                    print(temp_json)
                    # print(temp_json['topic'])
                    if temp_json['type'] == 'message':
                        curr_dt = datetime.utcfromtimestamp(temp_json['data']['time']/1000).strftime('%Y-%m-%d %H:%M:%S')
                        if temp_json['topic'] == '/market/ticker:all':
                            # Prep entry data for the DataFrame
                            msg_data = {
                                'exchange': 'kucoin',
                                'ticker': temp_json['subject'], 
                                'price': temp_json['data']['price'],
                            }
                            # Prep index for DataFrame
                            time_id = [curr_dt]
                        elif temp_json['topic'] in level_two_list:
                            # Prep entry data for DataFrame
                            msg_data = {
                                'exchange': ''
                                'ask price': ''
                            }
                    if self.queue_1.full():
                        print('working')
                    if self.queue_2.full():
                        print('working 2')
                    # If data is relevant, queue DataFrame
                    if msg_data != [] and time_id != []:
                        df = pd.DataFrame(data = msg_data, index = time_id)
                        self.queue_1.put(df)
                        # print('culture')
                    i += 1
                    
        except Exception:
            import traceback
            print(traceback.format_exc())

async def main():
    q = multiprocessing.Queue()
    r = multiprocessing.Queue()
    ws = kucoin_websocket_raw(q, r, topics = ['/market/ticker:all', '/market/level2:BTH-USDT'])
    ws.get_ws()
    await ws.get_id()
    ws.get_ws()
    await ws._run()


def run():
    asyncio.run(main())

run()