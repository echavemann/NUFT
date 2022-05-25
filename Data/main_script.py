import multiprocessing as mp
import concurrent.futures as cf
import BinanceClass as bc
import RawKucoinSocket as ks
import pandas as pd
import asyncio
from _thread import start_new_thread
import _thread

	
async def main():
	with cf.ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
		executor.submit(ks.run)
		executor.submit(bc.run)

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete((main()))

# Start all threads and ignore exit.
# async def main():
# 	q = mp.Queue()
# 	kucoinwebsocket = ks.kucoin_websocket_raw(q,['/market/ticker:all','/market/level2:BTC-USDT'])
# 	kucoinwebsocket.get_ws()
# 	await kucoinwebsocket.get_id()
# 	kucoinwebsocket.get_ws()
# 	binancewebsocket = bc.binance_websocket_raw(q,['BTCUSDT','ETHUSDT'])
# 	_thread.start_new_thread(binancewebsocket.run,(1,))

# def run():
# 	if __name__ == '__main__':
# 		asyncio.get_event_loop().run_until_complete((main()))

# run()
