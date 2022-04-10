import time
import pandas

from binance import ThreadedWebsocketManager


api_key = ''
api_secret = ''

def main():

    symbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT','GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']
    socket = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    socket.start()

    global current_list_of_dict
    current_list_of_dict = []
    global dict_count
    dict_count = 0
    global count
    count = 0

    def handle_socket_message(msg):
        # print(f"message type: {msg['e']}")
        global current_list_of_dict
        global dict_count
        global count
        del msg["M"]
        current_list_of_dict.append(msg)
        dict_count = dict_count + 1
        if dict_count > 100: 
            dict_count = 0
            df = pandas.DataFrame(current_list_of_dict)
            current_list_of_dict = []
            df.to_csv("TradaData"+str(count)+".csv")
            count = count + 1

    for i in range(len(symbols)):  
        socket.start_aggtrade_socket(callback=handle_socket_message, symbol=symbols[int(i)])
    socket.join()

main()

"""
HEADINGS
// Event type
// Event time
// Symbol
// Aggregate trade ID
// Price
// Quantity
// First trade ID
// Last trade ID
// Trade time
// Is the buyer the market maker?
// Ignore
"""