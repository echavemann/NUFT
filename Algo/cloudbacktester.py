import time
import csv
import os
import numpy
import pandas as pd
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import asyncio
from binance import ThreadedWebsocketManager
import nuftauth

kuCoin_api_key = ''
kuCoin_api_secret = ''
kuCoin_api_passphrase = ''
global loop

bsymbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT',
    'GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']

kcoins = bsymbols
for element in kcoins:
    if 'USDT' in element:
        element.replace('USDT','-USDT')
    
        
#awsclient = nuftauth.activate_aws('config.yaml')

delay = 0 #If we use delay, just need to stagger both the input of information and the order execution.
pendings = []
holdings = {}
orderbook = {}
pace = .1 #The pace of our tester. It is going to be 100ms by default, but maybe we should make it longer because Python is very slow. 
balance = 100000
allocation = 500


#pull all of the data from websockets, parse, process, store in a dictionary so that the marketorders can maybe possibly run this in decent time. 

#every 100ms, check the pending orders file, if there are any, add them to the pendings list/stack. 

#go through pendings, if the order is a sell but is not correlated with a holding, then just remove it. 

#call marketorder on every single one, using market orders for everything for now. 

#want to buy 5
#orderbook only has 3
#append same order to pendings with 5-3 quantity
('AAPL','buy',(5-3))
#Market order needs both the orders implemented but also we need to see what it's runtime is like, as well as hooking it up to the websocket data.
def marketorder(symbol, quantity, side):
    if side == 'buy':
        pass
    if side == 'sell':
        pass
#Errors:
#0 - Trade went through
#1 - Trade failed due to insufficient funds
#2 - Trade passed partially. 
#3 - Trade failed due to insufficient funds
