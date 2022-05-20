import asyncio
from asyncore import loop
from lib2to3.pygram import Symbols 
from binance import Client, BinanceSocketManager
import csv
import os
import datetime

coins = ['BTC-USDT', 'ETH-USDT']

class Binance_Websocket:
    def __init__(self, queue, symbols, api_key, api_secret):
        self.symbols = symbols
        self.queue = queue
        self.api_key = api_key
        self.api_secret = api_secret
    
    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        
    async def run(self):
        global loop
        loop = asyncio.get_event_loop()
        async def handle_evt(msg):
            coin = msg['subject']
            
            if coin in coins:
                print(msg)
                self.queue.put(msg)
                print(self.queue.qsize())
                
                
        client = Client(self.api_key, self.api_secret)
        bsm = await BinanceSocketManager.create(loop, client, handle_evt)
        await bsm.subscribe('trade', self.symbols)
        
        w