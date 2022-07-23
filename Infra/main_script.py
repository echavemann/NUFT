import multiprocessing as mp
import concurrent.futures as cf
import Binance_Websocket as bc
import Kucoin_Websocket as ks
import Coinbase_Websocket as cb
import Kraken_Websocket as kr
import Gemini_Websocket as gm
import pandas as pd
import asyncio

#All functions imported need to be non-async! If you commit async functions, our code will not work, and we will have an emergency debugging in your 'honor'.

#Stage code
async def main(coins):
	with cf.ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
	#NO SEMICOLONS!!
		executor.submit(ks.run)
		executor.submit(cb.run)
		executor.submit(bc.run)
		executor.submit(kr.run)
		executor.submit(gm.run)

#Run code
coins = []
if __name__ == '__main__':
	asyncio.get_event_loop().run_until_complete(main(coins))
