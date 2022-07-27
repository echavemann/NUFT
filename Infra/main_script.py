import multiprocessing as mp
import concurrent.futures as cf
import Binance_Websocket as bc
import Kucoin_Websocket_Formatted as ks
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
		q1 = mp.Queue()
		q2 = mp.Queue()
		df = pd.DataFrame(data = [])
		# kr = kr.Kraken_Websocket(coins)
		# cb = cb.Coinbase_Websocket(coins)
		ks_ws = ks.Kucoin_Websocket(q1, q2, topics = ['/market/ticker:' + ','.join(coins), '/market/level2:' + ','.join(coins)])
		# bc = bc.Binance_Websocket(coins)
		# gm = gm.Gemini_Websocket(coins)
		# temp_q1_rows = q1.get()
		# print(temp_q1_rows)
		# for row in temp_q1_rows:
		# 	pd.concat(df, row)
		# print(df)
		executor.submit(ks_ws._run_)
		executor.submit(print(q1.get()))

		# executor.submit(cb.run)
		# executor.submit(bc.run)
		# executor.submit(kr.run)
		# executor.submit(gm.run)

#Run code
coins = ['BTH-USDT']
def activate(coins):
	if __name__ == '__main__':
		asyncio.get_event_loop().run_until_complete(main(coins))

activate(coins)
