import asyncio
from time import time 
import websockets
import requests
import multiprocessing
import time
import json
from uuid import uuid4


class Kucoin_Websocket():
    
    def __init__(self,queue,topics = []):
        self.token = ''
        self.queue = queue
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

                while True:
                    message = await websocket.recv()
                    if self.queue.full():
                        print('working')
                    self.queue.put(message)
                    print('Kucoin')
        except Exception:   
            import traceback
            print(traceback.format_exc())

async def main():
    q = multiprocessing.Queue()
    ws = Kucoin_Websocket(q,['/market/ticker:all','/market/level2:BTC-USDT'])
    ws.get_ws()
    await ws.get_id()
    ws.get_ws()
    await ws._run()

def run():
    asyncio.run(main())