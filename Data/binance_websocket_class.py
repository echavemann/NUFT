import pandas as pd
from binance import ThreadedWebsocketManager

class Binance_Websocket:

	def __init__(self, queue, symbols, api_key='', api_secret=''):
		self.symbols = symbols
		self.api_key = ''
		self.api_secret =''
		self.queue = queue

	def main(self, queue):

	    # list of channels that we are subscribing to
	    socket = ThreadedWebsocketManager(api_key=self.api_key, api_secret=self.api_secret)
	    socket.start()

	    # our handle method cannot take inputs other than message, so 
	    # variables have to be global. These variables exist for 
	    # storing response messages temporarily.

	    # this is a handle method that's called every time that
	    # we receive a message from the websocket
	    def handle_socket_message(msg):
	        # delete the useless ignore column, see below for a full
	        # list of headings of the response message
	        del msg["M"]
	        # once we have received 100 messages from Binance, pack
	        # the messages and store it to a local csv file. Then it's
	        # uploaded to our AWS.
	        df = pandas.DataFrame(msg)
	        self.queue.put(df)

	    # subscribe to the Binance websocket channels according to the
	    # symbols listed above
	    for i in range(len(self.symbols)):  
	        socket.start_aggtrade_socket(callback=handle_socket_message, symbol=self.symbols[int(i)])
	    socket.join()
