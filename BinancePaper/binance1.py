import time

from binance import ThreadedWebsocketManager

api_key = 'K09wfTo1uYFtl1cDRPEEvi81uHiVfk0U8Y1C5odk3Mrrc0Res6wSOQpMx64FpWnT'
api_secret = '9epZfHtrletlYq0r9uywHB5NqFBoIHxGzO4PeBykFQwgtU0deazpVrKtSapGffIy'

def main():

    symbols = ['BTCUSDT','ETHUSDT','LUNAUSDT','SOLUSDT','AVAXUSDT','GLMRUSDT','FTMUSDT','VRAUSDT','PYRUSDT','DOGEUSDT']
    socket = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    socket.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    for i in range(len(symbols)):  
        socket.start_aggtrade_socket(callback=handle_socket_message, symbol=symbols[int(i)])
    socket.join()

main()