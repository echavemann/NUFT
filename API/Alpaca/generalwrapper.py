import requests,json 
import config
import websocket, json
import alpaca-trade-api as tradeapi

#websocket is a package "websocket- client" pip3 websocket-client
def on_open(ws):
    print("opened")  #print open when running the socket 
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
    }
    ws.send(json.dumps(auth_data))
    #to send it a message as a json file to conver python disctionary to json file  

    listen_message = {"action": "listen","data":{"streams":["T.TSLA","T.AAPL"]}}
#to change what stocks you are receiving messages from just change the stream output 
    ws.send(json.dumps(listen_message))
    #gives all the trades, receive streaming data 
    
#after connecting can subscribe to a "ticker" by subscribing onto a channel("stock")


def on_message(ws,message):
    print("received a message")
    print(message)

#the socket which can be found in the alpaca documentation to connect to the makret data
socket = "wss://data.alpaca.markets/stream"
#we connect to the socket using the websocket app from the package


#can see what stocks are available to trade using...
active_assets = api.list_assets(status='active')


ws= websocket.WebSocketApp(socket, on_open=on_open,on_message=on_message)
ws.run_forever()
#each input to a function is in reference to what could happen when you connect using the socket, you open it, you receive messages,
#the websocket section is to stream data
#self-explanatory
def time_to_market_close():
	clock = api.get_clock()
	return (clock.next_close - clock.timestamp).total_seconds()

def wait_for_market_open():
	clock = api.get_clock()
	if not clock.is_open:
		time_to_open = (clock.next_open - clock.timestamp).total_seconds()
		sleep(round(time_to_open))

#getting account information using built in api system 
account = api.get_account()
print(account)

#getting a stock's information          
def get_historic_data(stock,day):
    barset=api.get_barset(stock,day)
    print(barset._raw)
#example of stock data return 
#get_historic_data('TSLA','15Min')
#15-minute closing price data for Tesla: 

#get up to data price for the symbol:
def current_price(stock):
    stock_bars = api.get_barset(stock, 'minute', 1).df.iloc[0]
    stock_price = stock_bars[stock]['close']
    print(stock_price)


