import s3lib
import time

#Pull resources from the cloud
# s3lib.download('level1.csv', 'nuft','level1data.csv')
# s3lib.download('tradedata.csv', 'nuft','level2data.csv')

pendings = []
holdings = {}
balance = 0
#Receipt Class


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
