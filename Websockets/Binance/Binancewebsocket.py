import time

from binance import ThreadedWebsocketManager

api_key = ''
api_secret = ''

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
