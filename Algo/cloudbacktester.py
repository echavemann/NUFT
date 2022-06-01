import time
import csv
import os
import numpy
import pandas as pd
import asyncio
import nuftauth
import csv
import os
import time


kuCoin_api_key = ''
kuCoin_api_secret = ''
kuCoin_api_passphrase = ''
global loop

# bsymbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT',
#     'GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']

# kcoins = bsymbols
# for element in kcoins:
#     if 'USDT' in element:
#         element.replace('USDT','-USDT')
    
        
#awsclient = nuftauth.activate_aws('config.yaml')

delay = 0 #If we use delay, just need to stagger both the input of information and the order execution.
pendings = [] # holds tuple, (symbol, side)
holdings = {} # holds symbol as keys, and the quantity as values.
level1 = {} #Holds symbol as keys, price as values. 
orderbook = {} 
pace = .1 #The pace of our tester. It is going to be 100ms by default, but maybe we should make it longer because Python is very slow. 
global balance
balance = 100000
allocation = 500




#pull all of the data from websockets, parse, process, store in a dictionary so that the marketorders can maybe possibly run this in decent time. 
def readlevel1():
    l1 = pd.read_csv('level1.csv')
    tck = l1['subject']
    dat = l1['data']
    for line in dat:
        dat.split(' ')
    level1[tck] = dat[9]


def readlevel2():
    l2 = pd.read_csv('level2.csv')
    orderbook[l2['s']] = l2['q']*l2['p']

#call this every pace*second seconds
def updatepending():
    df = pd.read_csv('orders.csv')
    os.remove('orders.csv')
    df.to_dict()
    for ticker in df:
        if (df[ticker] == 'buy') or (ticker in holdings):
            pendings.append((ticker, df[ticker])) 
        
        
# #Market order needs both the orders implemented but also we need to see what it's runtime is like, as well as hooking it up to the websocket data.
# def marketorder(symbol, quantity, side):
#     if side == 'buy':
#         l2 = pd.read_csv('level2.csv')
#         if l2['q'] < quantity:
#             pending_quant=quantity-l2['q']
#             change_balance =level1[symbol] * l2['q']
#             balance = balance - change_balance 
#             l2['q'] = pending_quant
#             holdings=holdings.append(
#                 pd.Series([symbol, change_balance,'N/A'],
#                 index = my_columns),
#                 ignore_index= True)
#             pendings = pendings.append(symbol,side,pending_quant)
            
#         else:
#             change_balance =level1[symbol] * quantity
#             l2['q']=l2['q']-quantity
#             balance = balance - change_balance 
#             holdings=holdings.append(
#                 pd.Series([symbol, change_balance,'N/A'],
#                 index = my_columns),
#                 ignore_index= True)        
#         #Check the orderbook, compute p*q,check bal, increment balance and holdings accordingly, pendings if required. 
#     if side == 'sell':
#         l2 = pd.read_csv('level2.csv')
#         pass
#         change_balance =level1[symbol] * quantity
#         balance = balance + change_balance 
#         holdings=holdings.append(
#             pd.Series([symbol, change_balance,'N/A'],
#             index = my_columns),
#             ignore_index= True)
#Errors:
#0 - Trade went through
#1 - Trade failed due to insufficient funds
#2 - Trade passed partially. 
#3 - Trade failed due to insufficient funds


# #call marketorder on every single one, using market orders for everything for now. 
# def execute():
#     for entry in pendings:
#         marketorder(entry[0], (allocation/level1[entry[0]]), entry[1])

# def main():
#     readlevel1()
#     readlevel2()
#     updatepending()
#     execute()
    
    
# while True:
#     main()
#     time.sleep(0.000001)
    #call everything we wrote and then run it forever lmao
