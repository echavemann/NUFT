import time
import pandas
import s3test

from binance import ThreadedWebsocketManager


api_key = ''
api_secret = ''

def main():

    # list of channels that we are subscribing to
    symbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT',
    'GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']
    # initialize the websocket client
    socket = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    socket.start()

    # our handle method cannot take inputs other than message, so 
    # variables have to be global. These variables exist for 
    # storing response messages temporarily.
    global current_list_of_dict
    current_list_of_dict = []
    global dict_count
    dict_count = 0


    # this is a handle method that's called every time that
    # we receive a message from the websocket
    def handle_socket_message(msg):
        global current_list_of_dict
        global dict_count
        # delete the useless ignore column, see below for a full
        # list of headings of the response message
        del msg["M"]
        current_list_of_dict.append(msg)
        dict_count = dict_count + 1
        # once we have received 100 messages from Binance, pack
        # the messages and store it to a local csv file. Then it's
        # uploaded to our AWS.
        if dict_count > 100: 
            dict_count = 0
            df = pandas.DataFrame(current_list_of_dict)
            current_list_of_dict = []
            df.to_csv("TradeData.csv")
            s3test.upload("TradeData.csv","nuft")

    # subscribe to the Binance websocket channels according to the
    # symbols listed above
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
