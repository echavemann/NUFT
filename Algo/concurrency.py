import concurrent.futures
import time 
import os

from numpy import var

#this assigns to each compute thread because threading is a lie

def sleep_abit(seconds):
    print(f'Sleeping {seconds} seconds(s)')
    time.sleep(seconds)
    print('waking up')
    print(seconds)
    return "Done sleeping"

secondslist = [3,5,15,20,2]

#execution time: 20.3, 20.42, 20.4, 20.3
start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        f1 = executor.map(sleep_abit, secondslist)
        
        
end = time.time()
print("Finished in time : ", end-start)


        