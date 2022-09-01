import concurrent.futures as cf
import multiprocessing as mp
import Kucoin.Kucoin_Websocket as ks
import Coinbase.Coinbase_Websocket as cb
import Gemini.Gemini_Websocket_Formatted as gm
import Binance.Binance_Websocket as bc
# import Kraken.Kraken_Websocket as kr
import pandas as pd
import asyncio
import schedule
import datetime
import os

# from Infra.Binance_Websocket import Binance_Websocket
# from Infra.Coinbase_Websocket import Coinbase_Websocket

# All functions imported need to be non-async! If you commit async functions, our code will not work, and we will have an emergency debugging in your 'honor'.

# Stage code:
async def main(coins):
    with cf.ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        # NO SEMICOLONS!!
        q1 = mp.Queue()
        q2 = mp.Queue()
        lock = mp.Lock()
        df = pd.DataFrame(data=[])

        current_df = None

        # Stage 1: setting up all the websockets
        # input coins: a list of all coins
        binance = bc.Binance_Websocket(q1, q2, coins)
        coinbase = cb.Coinbase_Websocket(q1, q2, coins)
        for each_coin in coins:
            # kraken = kr.Kraken_Websocket(
            #     q1, q2, topics=['/market/ticker:all', '/market/level2:BTC-USDT'])
            gemini = gm.Gemini_Websocket(q1, 'wss://api.gemini.com/v1/multimarketdata?symbols=' + ','.join(each_coin), each_coin)
            ks_ws = ks.Kucoin_Websocket(q1, q2, lock, coins=['/market/ticker:' + ','.join(each_coin), '/market/level2:' + ','.join(each_coin)])

            # Stage 2: running all the websockets
            print('before')
            try:
                executor.submit(ks_ws._run_)
                print('running kucoin')
            except Exception:
                try:
                    executor.submit(coinbase.run)
                    print('running coinbase')
                except Exception:
                    try:
                        executor.submit(binance.run)
                        print('running binance')
                    except Exception:
                        # try:
                        #     executor.submit(kraken.run)
                        # except Exception:
                        executor.submit(gemini.run)
                        print('running gemini')
            print('after')
            try:
                lock.acquire()
                print('q1 output: ' + q1.get())
                lock.release()
            except:
                print('empty')
            print('outside')
            # try:
            #     print('rows')
            #     print(q1.qsize())
            #     row = q1.get()
            #     if row == None:
            #         break
            #     print(row)
            #         # print(row)
            # except:
            #     print('oh shit')
            print('outside')            
        # schedule.every(3).seconds.do(current_df = make_df(q1))
        # schedule.every(3).seconds.do(save_df(current_df))
        # while True:
        #     schedule.run_pending()

# Run code
coins = ['BTH-USDT']


def activate(coins):
    if __name__ == '__main__':
        asyncio.get_event_loop().run_until_complete(main(coins))


activate(coins)
