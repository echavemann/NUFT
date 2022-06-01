import time
import os
import multiprocessing
import nuftauth

#Tests on real time data from websockets. 
class RTBacktester():
    
    def __init__(self, queue, balance = 100000, allocation = 500):
        self.pendings = []
        self.inputqueue = queue
        self.orderqueue = multiprocessing.Queue()
        self.holdings = {}
        self.level1 = {}
        self.orderbook = {}
        self.balance = balance
        self.allocation = allocation
    
    def prime(self):
        #Start reading data from websockets, start storing in level1 and orderbook. 
        pass
    
    def run(self):
        #crunch crunch crunch
        pass
        
#Reads CSVs and tests backwards. 
class HistBacktester():
    
    def __init__(self, balance = 100000, allocation = 500, rate = 0.1):
        self.pendings = []
        self.holdings = {}
        self.level1 = {}
        self.orderbook = {}
        self.balance = balance
        self.allocation = allocation
        self.rate = rate
    
    def prime(self):
        pass
    
    def run(self):
        pass