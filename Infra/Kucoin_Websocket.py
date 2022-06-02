import asyncio
from time import time 
import websockets
import requests
import multiprocessing
import time
import json
from uuid import uuid4


class kucoin_websocket_raw():
    
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
            async with websockets.connect(self.wsendpoint) as websocket:
                for topic in self.topics:
                    await websocket.send(json.dumps({
                        "id": self.connectid,
                        "type": 'subscribe',
                        "topic": topic,
                        "response": True
                    }))
                #if time.time() - self.last_ping > self.timeout:
                await websocket.send(json.dumps({
                        "id": self.connectid,
                        "type": 'ping'
                }))
                self.last_ping = time.time()
                
                
                while True:
                    message = await websocket.recv()
                    self.queue.put(message)
                    print('Kucoin')
        except Exception:
            import traceback
            print(traceback.format_exc())

# r = requests.post('https://api.kucoin.com/api/v1/bullet-public')
# r = r.json()
# token = r['data']['token']
# endpoint = r['data']['instanceServers'][0]['endpoint']
# connectid = str(uuid4()).replace('-', '')
# wsendpoint = f"{endpoint}?token={token}&connectId={connectid}"
# websockets.connect(endpoint)

async def main():
    q = multiprocessing.Queue()
    ws = kucoin_websocket_raw(q,['/market/ticker:all','/market/level2:BTC-USDT'])
    ws.get_ws()
    print(ws.wsendpoint)
    await ws.get_id()
    ws.get_ws()
    await ws._run()

def run():
    asyncio.run(main())