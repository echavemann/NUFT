import multiprocessing as mp
import concurrent.futures as cf
import BinanceClass as bc
import RawKucoinSocket as ks
import pandas as pd
import asyncio
	
async def main():
	with cf.ProcessPoolExecutor() as executor:
		q = mp.Queue()
		kucoinwebsocket = ks.kucoin_websocket_raw(q,['/market/ticker:all','/market/level2:BTC-USDT'])
		kucoinwebsocket.get_ws()
		await kucoinwebsocket.get_id()
		kucoinwebsocket.get_ws()
		binancewebsocket = bc.binance_websocket_raw(q,['BTCUSDT','ETHUSDT'])
		# executor.submit(kucoinwebsocket.start())
		executor.submit(await binancewebsocket.run())
		executor.submit(await kucoinwebsocket.run())

if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main())
