
import pandas as pd
from kucoin import ThreadedWebsocketManager


class Kucoin_Socket:

    def __init__ (self,queue,symbols, api_key = '', api_secret = ''):
        self.queue = queue
        self.symbols = symbols

    def main(self):
        socket = ThreadedWebsocketManager(api_key = self.api_key, api_secret = self.api_secret)
        socket.start()

        def handle_socket_message(msg):
            
            del msg["M"]

            self.queue.put(msg)
        

        for i in range(len(self.symbols)):
            socket.subscribe_to_market_data(self.symbols[i])
        socket.join()





