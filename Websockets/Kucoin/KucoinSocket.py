from asyncore import loop
import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

api_key = ''
api_secret = ''
api_passphrase = ''

coins = ['BTC-USDT', 'ETH-USDT']

async def main():
    global loop
        #This needs to be a dictionary powered by key piars
    async def handle_evt(msg):
        coin = msg['subject']
        if coin in coins:
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
