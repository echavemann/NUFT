import ccxt
#from kucoin.client import Client
import nuftauth
import multiprocessing as mp
import pandas as pd

#backtester class needs to take in a mp.Queue
#try-except for the queue read
#akes in order queue (AAPL,2)
#output confirmation queue
#('buy/sell', USD, symbol)

exchanges = {'Binance':2}
#2 connotes only api and secret. 
#3 Connotes api, secret, uid
#4 Connotes api, secret, uid, and password
#5 Connotes api,secret, password

active = {}
#active values are 


#for each exchange, run the following processes:
def activate_binance():
    binance = ccxt.binance()
    binance.apiKey = ''
    binance.secret = ''
    active['Binance'] = binance
#General orders: 
#order = binance.create_order(symbol='BTC/USDT', type='limit', side='buy', amount=0.01, price=0.000001)
#createOrder(order)

def placeorder(exchange:str, symbol:str, type:str, side:str, amount, price):
    if exchange not in exchanges:
        exit('Exchange not supported by NUFT.')
    if exchange not in active.values():
        exit('Exchange not activated.')
    #check if they have that type of order
    broker = active[exchange]
    if type == 'market':
        if broker.has['createMarketOrder']:
            order = broker.create_order(symbol=symbol, type=type, side=side, amount=amount)
            #changed to multiple return value
            return 0,order
        else:
            #changed to multiple return value
            return 1,None


#activate all the brokerage
#While true
#read queue, call placeorder. 
#Put confirmation another queue

#some magical input queue
def main(queue):
    #activate all the brokerage
    activate_binance()
    #create a queue for results
    result_queue = []
    #while true
    while(queue.qsize() > 0):
        # need to know the order of the queue
        #reading the queue
        cur_data = queue.dequeue()
        #the indexing is wrong, modify this based on the order of the queue
        exchange = cur_data[0]
        symbol = cur_data[1]
        type = cur_data[2]
        side = cur_data[3]
        amount = cur_data[4]
        # call placeorder
        returned_indicator, order = placeorder(exchange, symbol, type, side, amount)
        if returned_indicator == 0:
            result_queue.append(order)
        if result_queue.__len__ == queue.qsize(): 
            df = pd.DataFrame(result_queue)
            result_queue = []
            df.to_csv("Confirmation Queue.csv")
    
    
        
    
    
