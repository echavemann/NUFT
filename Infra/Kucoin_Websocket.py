import asyncio
import websockets
import requests
import multiprocessing as mp
import json
from uuid import uuid4

class kucoin_websocket():
    def __init__(self, queue, topics = []):
        self.queue = queue
        self.topics = topics
        
        self.sessionID, self.wsEndPoint, self.timeOut = self._getWSEndpoint()
        self.MSG = self._getMSG()
        asyncio.run(self._run())

    def _getWSEndpoint(self):
        x = requests.post('https://api.kucoin.com/api/v1/bullet-public').json()
        token = x['data']['token']
        server = x['data']['instanceServers'][0]["endpoint"]
        id = str(uuid4()).replace('-', '')
        return str(uuid4()).replace('-', ''), server + '?token=' + token + '&[connectId=' + id + ']', int(x['data']['instanceServers'][0]['pingInterval'] / 1000) - 1

    def _getMSG(self):
        temp = []
        for i in self.topics:
            temp.append({'id': self.sessionID, 'type': 'subscribe', 'topic': i, 'response': True})
        return temp
    
    async def _run(self):
        async with websockets.connect(self.wsEndPoint, ping_interval=self.timeOut, ping_timeout=None) as websocket:
            for i in self.MSG:
                await websocket.send(json.dumps(i))
            while True:
                message = await websocket.recv()
                if self.queue.full():
                    print("Queue is Full")
                self.queue.put(message)
                print(message)

a = kucoin_websocket(mp.Queue(), ['/market/ticker:all','/market/level2:BTC-USDT'])