
import websocket, json
symbol = "btcusd"
socket = "wss://stream.binance.com:9443/ws/{symbol}@aggTrade"

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

websocket.enableTrace(True)
ws = websocket.WebSocketApp(socket,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close
)

ws.run_forever()