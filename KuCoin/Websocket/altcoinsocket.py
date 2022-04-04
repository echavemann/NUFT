from asyncore import loop
import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

api_key = ''
api_secret = ''
api_passphrase = ''

async def main():
    global loop
        #This needs to be a dictionary powered by key piars
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

        elif msg['topic'] == '/market/ticker:DOGE-USDT' :
            print(f'got DOGE-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:FTM-USDT' :
            print(f'got FTM-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:VRA-USDT' :
            print(f'got GLMR-USDT tick: {msg["data"]}')

        elif msg['topic'] == '/market/ticker:PYR-USDT' :
            print(f'got GLMR-USDT tick: {msg["data"]}')
        elif msg['topic'] == '/market/ticker:all' :
            print(f'got arguably useless data: {msg["data"]}')
        
        

    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    #ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)
    #Can conjugate for runtime
    await ksm.subscribe('/market/ticker:ETH-USDT')
    await ksm.subscribe('/market/ticker:BTC-USDT')
    await ksm.subscribe('/market/ticker:LUNA-USDT')
    await ksm.subscribe('/market/ticker:SOL-USDT')
    await ksm.subscribe('/market/ticker:AVAX-USDT')
    await ksm.subscribe('/market/ticker:GLMR-USDT')
    await ksm.subscribe('/market/ticker:DOGE-USDT')
    await ksm.subscribe('/market/ticker:FTM-USDT')
    await ksm.subscribe('/market/ticker:VRA-USDT')
    await ksm.subscribe('/market/ticker:PYR-USDT')
    #await ksm.subscribe('/market/ticker:all')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20, loop=loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
