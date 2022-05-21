import asyncio
from asyncore import loop
from lib2to3.pygram import Symbols 
from binance import AsyncClient, BinanceSocketManager
import csv
import os
import multiprocessing as mp
import datetime

class Binance_Websocket:

    def __init__(self, queue, symbols=['BTCUSDT'], api_key='', api_secret=''):
        self.queue = queue
        self.api_key = api_key
        self.api_secret = api_secret
        # binance has some weird rules about their symbols, and we need to 
        # attach sth to every symbol. Then we start a multiplex socket with 
        # the modified list of symbols.
        self.symbols = self.generate_symbols(symbols)
    
    def generate_symbols(self,symbols):
        s = []
        for symbol in symbols: 
            s.append(symbol.lower()+'@ticker')
        return s

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        
    async def run(self):
        global loop
        loop = asyncio.get_event_loop()

        # async def handle_evt(msg):            
        #     # print(msg)
           
        
        # start the multiplex socket
        client = await AsyncClient.create(self.api_key, self.api_secret)
        bm = BinanceSocketManager(client)
        sockets = bm.multiplex_socket(self.symbols)

        # the following stuff just print the results on your console and 
        # does nothing else
        async with sockets as s:
            while True:
                res = await s.recv()
                self.queue.put(res)
                print(self.queue.qsize())

def main():
    q = mp.Queue()
    coins = ['BTCUSDT', 'ETHUSDT']
    binance = Binance_Websocket(q,coins)
    binance.start()

if __name__ == '__main__':
    main()