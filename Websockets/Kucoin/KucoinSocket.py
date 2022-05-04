from asyncore import loop
import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("api_key")
api_secret = os.environ.get("api_secret")
api_passphrase = os.environ.get("api_passphrase")

coins = ['BTC-USDT', 'ETH-USDT']

async def main():
    global loop
        #This needs to be a dictionary powered by key pairs
    async def handle_evt(msg):
        coin = msg['subject']
        
        if coin in coins:
            today = datetime.today().strftime('%Y-%m-%d')
            file_path = f'Websockets/Kucoin/data/{coin} {today}.csv'
            with open(file_path, 'a') as f:
                writer = csv.writer(f)
                cols = [None]*8
                i = 0
                
                for value in msg["data"].values():
                    cols[i] = value
                    i += 1
                writer.writerow(cols)
                
            # val = (coin, msg["data"])
            #Store val in S3
        
    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    await ksm.subscribe('/market/ticker:all')


    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
