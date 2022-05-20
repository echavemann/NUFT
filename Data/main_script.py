import multiprocessing as mp
import KucoinClass as kc
import pandas as pd
import queue_fix

if __name__ == '__main__':
	mp.set_start_method('spawn')
	q = mp.Queue()
	websocket = kc.Kucoin_Websocket(q,['BTC-USDT', 'ETH-USDT'])
	p = mp.Process(target=websocket.start())
	p.start()
