from asyncore import loop
import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

api_key = ''
api_secret = ''
api_passphrase = '694207'

async def main():
    global loop

    async def handle_evt(msg):
        if msg['topic'] == '/market/ticker:ETH-USDT' :
            print(f'got ETH-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:BTC-USDT' :
            print(f'got BTC-USDT tick: {msg["data"]}')
            
        elif msg['topic'] == '/market/ticker:LUNA-USDT' :
            print(f'got LUNA-USDT tick: {msg["data"]}')
        
        elif msg['topic'] == '/market/ticker:SOL-USDT' :
            print(f'got SOL-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:AVAX-USDT' :
            print(f'got AVAX-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:GLMR-USDT' :
            print(f'got GLMR-USDT tick: {msg["data"]}')

        elif msg['topic'] == 'market/snapshot:BTC':
            print(f'got BTC market snapshot:{msg["data"]}')
        

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    #ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

    await ksm.subscribe('/market/ticker:ETH-USDT')
    await ksm.subscribe('/market/ticker:BTC-USDT')
    await ksm.subscribe('/market/ticker:LUNA-USDT')
    await ksm.subscribe('/market/ticker:SOL-USDT')
    await ksm.subscribe('/market/ticker:AVAX-USDT')
    await ksm.subscribe('/market/ticker:GLMR-USDT')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20, loop=loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
