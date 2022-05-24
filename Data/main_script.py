import multiprocessing as mp
import concurrent.futures as cf
import KucoinClass as kc
import BinanceClass as bc
import pandas as pd


coins = ['BTC-USDT', 'ETH-USDT']

#doe
    

if __name__ == '__main__':
	with cf.ProcessPoolExecutor() as executor:
		q = mp.Queue()
		kucoinwebsocket = kc.Kucoin_Websocket(q,coins)
		binancewebsocket = bc.binance_websocket_raw(q,coins)
		#executor.submit(kucoinwebsocket.start())
		executor.submit(binancewebsocket.run())
		#executor.submit(binancewebsoocket.start())
		#p.start()
