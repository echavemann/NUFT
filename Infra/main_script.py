import multiprocessing as mp
import concurrent.futures as cf
import Binance_Websocket_Formatted as bc
# from Infra.Binance_Websocket import Binance_Websocket
# from Infra.Coinbase_Websocket import Coinbase_Websocket
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

		#Stage 1: setting up all the websockets
		binance = bc.Binance_Websocket(q1, coins)
		coinbase = cb.Coinbase_Websocket(q1, 'wss://ws-feed.exchange.coinbase.com', coins, channels = ["ticker"])
		kraken = kr.Kraken_Websocket(q1, q2, topics = ['/market/ticker:all', '/market/level2:BTC-USDT'])
		gemini = gm.Gemini_Websocket(q1, q2, 'wss://api.gemini.com/v1/multimarketdata?symbols=' + ','.join(coins) , 'wss://api.gemini.com/v2/marketdata', coins)
		ks_ws = ks.Kucoin_Websocket(q1, q2, topics = ['/market/ticker:' + ','.join(coins), '/market/level2:' + ','.join(coins)])
		# temp_q1_rows = q1.get()
		# print(temp_q1_rows)
		# for row in temp_q1_rows:
		# 	pd.concat(df, row)
		# print(df)

		#Stage 2: running all the websockets
		try:
			executor.submit(ks_ws._run_)
		except Exception:
			try:
				executor.submit(coinbase.run)
			except Exception:
				try:
					executor.submit(binance.run)
				except Exception:
					try:
						executor.submit(kraken.run)
					except Exception:
						executor.submit(gemini.run)

#Run code
coins = ['BTH-USDT']
def activate(coins):
	if __name__ == '__main__':
		asyncio.get_event_loop().run_until_complete(main(coins))

activate(coins)
