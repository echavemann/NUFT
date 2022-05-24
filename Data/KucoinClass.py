import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import csv
from datetime import datetime
import os

coins = ['BTC-USDT', 'ETH-USDT']

class Kucoin_Websocket:
    def __init__(self,queue,symbols='', api_key='', api_secret='', api_passphrase = ''):
        self.symbols = symbols
        self.queue  = queue
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
    
    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        
    async def run(self):
        global loop
        loop = asyncio.get_event_loop()
        #This needs to be a dictionary powered by key pairs
        async def handle_evt(msg):
            coin = msg['subject']
            #coin2 = msg['data']['symbol']
            #print(coin)
            if coin in coins :
                print(msg)
                self.queue.put(msg)
                
            # val = (coin, msg["data"])
            #Store val in S3
        
        client = Client(self.api_key, self.api_secret, self.api_passphrase)

        ksm = await KucoinSocketManager.create(loop, client, handle_evt)

        await ksm.subscribe('/market/ticker:all')
        await ksm.subscribe('/market/level2:BTC-USDT')
        await ksm.subscribe('/market/level2:ETH-USDT')


        while True:
            print("sleeping to keep loop open")
            await asyncio.sleep(20)

# def main():
#     coins = ['BTC-USDT', 'ETH-USDT']
#     kucoin = Kucoin_Websocket(coins)
#     kucoin.start()

# if __name__ == '__main__':
#     main()

