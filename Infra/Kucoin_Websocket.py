import asyncio
from time import time 
import websockets
import requests
import multiprocessing
import time
import json
from uuid import uuid4
import time

'''
Usage Instructions:
    1.  from Kucoin_Websocket import kuCoin_WS
    2.  kuCoin_WS(
            {queue_name}, type is mp.Queue(),
            {tickers}, type is python list w/ multiple items separated by comma
        )
'''

class kuCoin_WS():
    def __init__(self, queue:mp.Queue(), topics:list) -> None:
        self.queue = queue
        self.topics = topics
        self.start = time.time()
        
        self.sessionID, self.wsEndPoint, self.timeOut, self.MSG = self._getWSEndpoint()
        asyncio.run(self._run())

    def _getWSEndpoint(self) -> tuple:
        x = requests.post('https://api.kucoin.com/api/v1/bullet-public').json()
        token = x['data']['token']
        server = x['data']['instanceServers'][0]["endpoint"]
        id = str(uuid4()).replace('-', '')

        temp = []
        for i in self.topics:
            temp.append({'id': id, 'type': 'subscribe', 'topic': i, 'response': True})

        return str(uuid4()).replace('-', ''), server + '?token=' + token + '&[connectId=' + id + ']', int(x['data']['instanceServers'][0]['pingInterval'] / 1000) - 1, temp

    def _addToQueue(self, q:mp.Queue(), data:str) -> None:
        if not q.full():
            q.put(data)
            print(data)
        else:
            q.get()
            q.put(data)
            print(data)

    async def _run(self) -> None:
        async with websockets.connect(self.wsEndPoint, ping_interval=self.timeOut, ping_timeout=None) as websocket:
            for i in self.MSG:
                await websocket.send(json.dumps(i))
            
            while True:
                message = await websocket.recv()
                self._addToQueue(self.queue, message)

kuCoin_WS(mp.Queue(), ['/market/ticker:all','/market/level2:BTC-USDT'])