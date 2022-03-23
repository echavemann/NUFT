import ibapi as ib
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import numpy as np
import pandas as pd

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
    def tickPrice(self,reqId,tickType,price,attrib):
        if tickType == 2 and reqId == 1:
            print('The current ask price is ',price)
    def nextValidId(self, orderID: int):
        super().nextValidId(orderID)
        self.nextValidId = orderID
        print('The next valid order ID is: ', self.nextorderId)
    def orderStatus(self,orderId, status, filled, remaining, avgFullPrice, permId, parentId,lastFillPrice,clientId,whyHeld,mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
    def execDetails(self, reqId, contract, execution):
	    print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    

def run_loop():
    app.run()


app = IBapi()
app.connect() #some shit
app.nextorderId = None
api_thread = threading.Thread(target=run_loop, daemon = True)
api_thread.start()
while True:
	if isinstance(app.nextorderId, int):
		print('connected')
		break
	else:
		print('waiting for connection')
		time.sleep(1)

time.sleep(0.5)

tesla_constract = Contract()
tesla_constract.symbol = 'TSLA'
tesla_constract.secType = 'STK'
tesla_constract.exchange = 'SMART'
tesla_constract.currency = 'USD'

app.reqMktData(1, tesla_constract, '', False, False, [])

order = Order()
order.action = 'BUY'
order.totalQuantity = 100000
order.orderType = 'LMT'
order.lmtPrice = '1.10'
order.orderId = app.nextorderId
app.nextorderId += 1
order.transmit = False

def FX_order(symbol):
	contract = Contract()
	contract.symbol = symbol[:3]
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = symbol[3:]
	return contract

app.placeOrder(order.orderId, FX_order('EURUSD'), order)

time.sleep(10)

app.disconnect()
