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

async def main():
    global loop
        #This needs to be a dictionary powered by key piars     
        # callback function that receives messages from the socket
    async def handle_evt(msg):
        if msg['topic'] == '/market/ticker:BTC-USDT':
            # print(f'got BTC-USDT tick:{msg["data"]}')
            global lst_of_ticker
            lst_of_ticker.append(msg)
            if len(lst_of_ticker) >= 100:
                global batchSize
                batchSize += 1
                print(batchSize)
                df = pd.DataFrame(lst_of_ticker)
                df.to_csv('KucoinData.csv')
                df.to_csv('/Users/frank/NUFT/KuCoin/BTCData.csv')
                lst_of_ticker = []


        #Store val in S3
        

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # await ksm.subscribe('/market/ticker:all')
    await ksm.subscribe('/market/ticker:BTC-USDT')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20, loop=loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


#Creating Session With Boto3.
session = boto3.Session(
    aws_access_key_id='<>',
    aws_secret_access_key='<>'
)

#Creating S3 Resource From the Session.
s3 = session.resource('s3')
txt_data = b'Coin Data from KuCoin'
object = s3.Object('<Coin Data>', 'file_name.txt')
result = object.put(Body=txt_data)
