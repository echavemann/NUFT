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
coins = ['BTC-USDT']

async def main():
    global loop
        #This needs to be a dictionary powered by key piars
    async def handle_evt(msg):
        coin = msg['subject']
        if coin in coins:
            # rows = f'got {coin} information: {msg["data"]["price"]}'
            # From data frame to CSV
            fields = ['Coin', 'Price', 'bestAsk', 'bestAskSize', 'bestBid', 'bestBidSize', 'size', 'sequence']
            filename = "coin_data.csv"
            coinPrice = msg["data"]['price']
            bestAsk = msg["data"]['bestAsk']
            bestAskSize = msg["data"]['bestAskSize']
            bestBid = msg["data"]['bestBid']
            bestBidSize = msg["data"]['bestBidSize']
            size = msg["data"]['size']
            sequence = msg["data"]['sequence']
            line = [[str(coin), str(coinPrice), str(bestAsk), str(bestAskSize), str(bestBid), str(bestBidSize), str(bestBidSize), str(size), str(sequence)]]
            print(coin)
            print(coinPrice)
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                # csvwriter.writerow([coin,coinPrice, bestAsk, bestAskSize, bestBid, bestBidSize, size, sequence])
                csvwriter.writerow(line)
                csvwriter.writerow('\n')
            print(f'got {coin} information: {msg["data"]}')
        val = (coin, msg["data"])


        #Store val in S3
        

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    await ksm.subscribe('/market/ticker:all')

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
