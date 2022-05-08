import multiprocessing as mp
import binance_websocket_class as bwc
import pandas as pd

if __name__ == '__main__':
	q = mp.Queue()
	websocket = bwc.Binance_Websocket(q,['BTCUSDT'])
	p = mp.Process(target=websocket.main(), args=(q))
	p.start()

