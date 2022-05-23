import ccxt
import kucoin
import nuftauth
import multiprocessing as mp

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
    binance.apiKey = 'BINANCEAPIKEY'
    binance.secret = 'BINANCESECRET'
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
            return 0
        else:
            return 1


#activate all the brokerage
#While true
#read queue, call placeorder. 
#Put confirmation another queue
    
        
    
    
