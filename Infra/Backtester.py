
'''
order = {
    "time" = {unix timestamp, in seconds}, 
    "price“ = {float = Any > 0}, 
    "volume" = {float = number of the crpto}, Example - in the BTC-USDT pair, would be the amount of BTC sold or bought
    "mode" = {str = "Buy", or "Sell"}, 
}

Price follows KuCoin's standard at endpoint '/api/v1/market/orderbook/level1'
OrderBook follows Binance's standard at endpoint '/api/v3/depth'
'''


'''
A few things to be aware of:
- Async may not work
- since getting data and execution is done sequentially, there might be lags (addressed by raised exceptions)
- This theortically works but has NOT BEEN TESTED

'''

import asyncio
import multiprocessing as mp
import time

class Backtester():
    
    def __init__(self, orderQueue, priceQueue, orderBookQueue, orderTimeout, tradeCountToStop):
        # orderTimeout -> time to discard a order (in seconds)
        # tradeCountToStop -> amount of trades for the backtester (int)
        
        self.currCoin = 0
        self.currStable, self.currStableinCrypto = 100
        self.tradeNum = 0
        self.timeOut = orderTimeout
        self.tradeNumMax = tradeCountToStop
        
        self.orderQueue = mp.Queue(orderQueue)
        self.priceQueue = mp.Queue(priceQueue)
        self.orderBook = mp.Queue(orderBookQueue)
        self.currOrder = ''
        
        self.orderList = []
        self.currCoinPrice = ''
        self.currOrderBook = ''
    
    '''
    - gets the new order, if there is one
    - gets the current coin price, and the newest order book
    - calcualte how much our stablecoin would be worth in crypto terms (since the trade volume is in crypto)
    essentially one function to put a few very common things together
    '''
    def refreshInfo(self):                                              #refreshes currOrders, currPrice and currOrderBook
        if not self.orderQueue.empty():
            self.orderList.append(self.orderQueue.get())
        self.currCoinPrice = self.priceQueue.get()['price']
        self.currOrderBook = self.orderBook.get()
        self.currStableinCrypto = self.currStable/self.currCoinPrice


    '''
    Gets the newest order, essentially, and resizes the list of backlogged orders
    Gets orders based on these condition:
        - Earliest
        - Not Timed Out
        - If buy, volume not larger than what we could afford
        - If sell, volume not larger than what we have
    returns -1 if there is no order avail
    '''
    def findCurrOrder(self):                                            #order will be executable (within resonable amount, and under the time limit)
        self.refreshInfo()
        count = 0
        for i in self.orderList:
            count += 1
            if time.time() - i["time"] > self.timeOut:
                if i['mode'] == 'Buy':
                    self.currCoinPrice = self.priceQueue.get()['price']             # another update, since it is HFT lol
                    self.currStableinCrypto = self.currStable/self.currCoinPrice
                    if i['volume'] <= self.currStableinCrypto:
                        self.orderList = self.orderList[count:]
                        return i

                elif i['mode'] == 'Sell':
                    if i['volume'] <= self.currCoin:
                        self.orderList = self.orderList[count:]
                        return i

        self.orderList = []
        return -1 #if no avail orders in the queue

    '''
    Does the trading thing, subtract from the sold equity and adds to the bought equity, basically keeping a balance sheet
    Again, wrote another test for if price changed a lot and we can't afford/sell it anymore
    '''
    def trade(self, mode, vol, price):
        if mode == "Buy":
            self.currCoin += vol
            if self.currStable - price * vol >= 0:
                self.currStable -= price * vol
            else:
                self.currStable = 0
                raise Exception("Buying more than we could afford??")

        elif mode == "Sell":
            if self.currCoin - vol >= 0:
                self.currCoin -= vol
            else:
                self.currCoin = 0
                raise Exception("Selling more than inventory??")

            self.currStable += price * vol
    
    '''
    'The Main Function'
    it gets an order, and executes it based on the orderbook until it times out
    if partially/fully executed, will note in output
    return 1 -> Full Exec
    return -1 -> Partial Exec
    return -2 -> No Exec
    return -3 -> No avail Order 
    '''
    def execute(self):                                                      # goes through the order book and sees if the trade could work
        self.refreshInfo()
        currOrder = self.findCurrOrder()
        orderVol = currOrder['volume']
        OrderPrice = currOrder['price']

        if currOrder != -1:
            while time.time() - currOrder["time"] > self.timeOut:
                self.refreshInfo()
                if currOrder['mode'] == 'Buy': #mode
                    for i in self.orderBook['asks'][0]:
                        if OrderPrice >= i[0]:
                            if orderVol <= i[1]: #fully traded
                                self.trade("Buy", i[1], i[0])
                                print ("Order ", currOrder, " was completed")
                                self.tradeNum += 1 
                                return 1 #success
                            
                            elif orderVol > i[1]:
                                self.trade("Buy", i[1], i[0])
                                orderVol -= i[1]

                elif currOrder['mode'] == 'Sell':
                    for i in self.orderBook['bids'][0]:
                        if OrderPrice <= i[0]:
                            if orderVol <= i[1]: #fully traded
                                self.trade("Sell", i[1], i[0])
                                print ("Order ", currOrder, " was completed")
                                self.tradeNum += 1 
                                return 1 #success
                            
                            elif orderVol > i[1]:
                                self.trade("Sell", i[1], i[0])
                                orderVol -= i[1]
            
            if orderVol == currOrder['volume']:
                print("Order ", currOrder, " timed out and was not traded")
                return -2
            else:
                print("Order ", currOrder, " partially timed out and ", orderVol, " has not been traded.")
                self.tradeNum += 1 
                return -1
        print ("No Avail Order")
        return -3 #no avail order

    '''
    async -> so we can execute the new orders while the old ones are still being executed in another instance of 'execute()'?
    Or am I understanding this wrong?
    '''
    async def run(self):
        while self.tradeNum < self.tradeNumMax:
            await self.execute()
        
        print("Backtester Complete, Algo Result after ", self.tradeNumMax," trades: ", 100 - self.currStable + (self.currCoin * self.priceQueue.get()['price']), "%.")






