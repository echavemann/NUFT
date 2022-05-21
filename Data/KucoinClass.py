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
        
            if coin in coins:
                # today = datetime.today().strftime('%Y-%m-%d')
                # file_path = f'Websockets/Kucoin/data/{coin} {today}.csv'
                # with open(file_path, 'a',newline='') as f:
                #     writer = csv.writer(f)
                #     cols = [None]*8
                #     i = 0
                
                #     for value in msg["data"].values():
                #         cols[i] = value
                #         i += 1
                #     writer.writerow(cols)
                #print(msg)
                self.queue.put(msg)
                #print(self.queue.qsize())
                
            # val = (coin, msg["data"])
            #Store val in S3
        
        client = Client(self.api_key, self.api_secret, self.api_passphrase)

        ksm = await KucoinSocketManager.create(loop, client, handle_evt)

        await ksm.subscribe('/market/ticker:all')


        while True:
            print("sleeping to keep loop open")
            await asyncio.sleep(20)

# def main():
#     coins = ['BTC-USDT', 'ETH-USDT']
#     kucoin = Kucoin_Websocket(coins)
#     kucoin.start()

# if __name__ == '__main__':
#     main()

