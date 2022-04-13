import time
import pandas
from asyncore import loop
import asyncio
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
# modified from import nuftauth
import nuftauth
from binance import ThreadedWebsocketManager


binance_api_key = ''
binance_api_secret = ''
kuCoin_api_key = ''
kuCoin_api_secret = ''
kuCoin_api_passphrase = ''

# Global variables used to store kuCoin data
global lst_of_ticker
lst_of_ticker = []
global batchSize
batchSize = 0

async def main():

    # Binance Websocket

    # list of channels that we are subscribing to
    symbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT',
    'GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']
    # initialize the websocket client
    socket = ThreadedWebsocketManager(api_key=binance_api_key, api_secret=binance_api_secret)
    socket.start()

    # our handle method cannot take inputs other than message, so 
    # variables have to be global. These variables exist for 
    # storing response messages temporarily.
    global current_list_of_dict
    current_list_of_dict = []
    global dict_count
    dict_count = 0


    # this is a handle method that's called every time that
    # we receive a message from the websocket
    def handle_socket_message(msg):
        global current_list_of_dict
        global dict_count
        # delete the useless ignore column, see below for a full
        # list of headings of the response message
        del msg["M"]
        current_list_of_dict.append(msg)
        dict_count = dict_count + 1
        # once we have received 100 messages from Binance, pack
        # the messages and store it to a local csv file. Then it's
        # uploaded to our AWS.
        if dict_count > 100: 
            dict_count = 0
            df = pandas.DataFrame(current_list_of_dict)
            current_list_of_dict = []
            df.to_csv("TradeData.csv")
            # nuftauth.upload("TradeData.csv","nuft")

    # subscribe to the Binance websocket channels according to the
    # symbols listed above
    for i in range(len(symbols)):  
        socket.start_aggtrade_socket(callback=handle_socket_message, symbol=symbols[int(i)])
    socket.join()


    # KuCoin Websocket

    global loop
    async def handle_evt(msg):
        if msg['topic'] == '/market/ticker:BTC-USDT':
            # print(f'got BTC-USDT tick:{msg["data"]}')
            global lst_of_ticker
            lst_of_ticker.append(msg)
            if len(lst_of_ticker) >= 100:
                global batchSize
                batchSize += 1
                print(batchSize)
                df = pandas.DataFrame(lst_of_ticker)
                df.to_csv('KucoinData.csv')
                df.to_csv('/Users/frank/NUFT/KuCoinBinanceCombined/BTCDataKuCoin.csv')
                lst_of_ticker = []

    
    client = Client(kuCoin_api_key, kuCoin_api_secret, kuCoin_api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # await ksm.subscribe('/market/ticker:all')
    await ksm.subscribe('/market/ticker:BTC-USDT')

    while True:
        print("sleeping to keep loop open")
        await asyncio.sleep(20, loop=loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

main()



"""
HEADINGS
// Event type
// Event time
// Symbol
// Aggregate trade ID
// Price
// Quantity
// First trade ID
// Last trade ID
// Trade time
// Is the buyer the market maker?
// Ignore
"""
