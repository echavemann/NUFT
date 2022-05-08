import multiprocessing as mp
import binance_websocket_class as bwc
import pandas as pd

if __name__ == '__main__':
	q = mp.Queue()
	websocket = bwc.Binance_Websocket(q,['BTCUSDT'])
	p = mp.Process(target=websocket.main(), args=(q))
	p.start()

import multiprocessing as mp
q = mp.Queue()
q.put(2)
q.put(4)

elements = list()
while q.qsize():
    elements.append(q.get())
print(elements)