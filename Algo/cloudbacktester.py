import time
import csv
import os
import numpy
import pandas as pd

#This is going to be rewritten in go 100%, just because the runtime is going to be too slow. 

delay = 0 #If we use delay, just need to stagger both the input of information and the order execution.
pendings = []
holdings = {}
pace = .1 #The pace of our tester. It is going to be 100ms by default, but maybe we should make it longer because Python is very slow. 
balance = 0


#pull all of the data from websockets, parse, process, store in a dictionary so that the marketorders can maybe possibly run this in decent time. 

#every 100ms, check the pending orders file, if there are any, add them to the pendings list/stack. 

#go through pendings, if the order is a sell but is not correlated with a holding, then just remove it. 

#call marketorder on every single one, using market orders for everything for now. 



#Market order needs both the orders implemented but also we need to see what it's runtime is like, as well as hooking it up to the websocket data.
def marketorder(order,symbol, price, quantity, side):
    if side == 'buy':
        if order == 'market':
            #Check the orderbook, compute p*q,check bal, increment balance and holdings accordingly, pendings if required. 
            pass
        elif order == 'limit':
            #CHeck the orderbook, compute p*q, check bal, increment balance and holdings accordingly, pendings if required.
            pass
        pass
    if side == 'sell':
        #confirm we have the holdings for this
        if holdings[symbol] < quantity:
            return 1
        if order == 'market':
            #Check the orderbook, compute p*q,check bal, increment balance and holdings accordingly, pendings if required. 
            pass
        elif order == 'limit':
            #Check the orderbook, compute p*q,check bal, increment balance and holdings accordingly, pendings if required. 
            pass
        pass
#Errors:
#0 - Trade went through
#1 - Trade failed due to insufficient funds
#2 - Trade passed partially. 
#3 - Trade failed due to insufficient funds
