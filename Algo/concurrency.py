import concurrent.futures
import time 

def sleep_abit(seconds):
    print(f'Sleeping {seconds} seconds(s)')
    time.sleep(seconds)
    return "Done sleeping"
start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        f1 = executor.submit(sleep_abit, 5)
        f2 = executor.submit(sleep_abit, 15)
        print(f1.result())
        print(f2.result())
        
        
end = time.time()
print("Finished in time : ", start-end)


        