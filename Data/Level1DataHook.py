from asyncore import loop
import asyncio
import pandas as pd
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import boto3
import csv

api_key = ''
api_secret = ''
api_passphrase = ''

# coins = ['BTC-USDT', 'ETH-USDT']

global lst_of_ticker
lst_of_ticker = []
global batchSize
batchSize = 0
coins = ['BTC-USDT', 'ETH-USDT']
async def main():
    global loop
        #This needs to be a dictionary powered by key piars     
        # callback function that receives messages from the socket
    async def handle_evt(msg):
        coin = msg['subject']
        if coin in coins:
            # print(f'got BTC-USDT tick:{msg["data"]}')
            global lst_of_ticker
            lst_of_ticker.append(msg)
            if len(lst_of_ticker) >= 100:
                global batchSize
                batchSize += 1
                print(batchSize)
                df = pd.DataFrame(lst_of_ticker)
                df.to_csv('level1.csv')
                lst_of_ticker = []
        

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # await ksm.subscribe('/market/ticker:all')
    await ksm.subscribe('/market/ticker:all')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

