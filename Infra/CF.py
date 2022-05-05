import concurrent.futures as cf 
import multiprocessing as mp
import time
import Binancewebsocket
import KuCoinBinanceCombine


def run_script1():
    exec(open("Binancewebsocket.py").read())
    

def run_script2():
    exec(open("KuCoinBinanceCombine.py").read())
    
if __name__ == '__main__':
    with cf.ProcessPoolExecutor() as executor:
        f1 = executor.submit(run_script1)
        f2 = executor.submit(run_script2)


#Figure out how to communicate between KuCoin and Binance using multiprocessing.Queue()