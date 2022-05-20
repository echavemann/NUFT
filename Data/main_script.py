import multiprocessing as mp
import concurrent.futures as cf
import KucoinClass as kc
import pandas as pd
import queue_fix

if __name__ == '__main__':
	with cf.ProcessPoolExecutor() as executor:
		q = mp.Queue()
		websocket = kc.Kucoin_Websocket(q,['BTC-USDT', 'ETH-USDT'])
		p = executor.submit(websocket.start())
		p.start()
