from binance.client import Client
from datetime import datetime

def get_client():
    with open('binanceus_keys.txt', 'r') as f:
        api_key, api_secret = f.read().splitlines()

    client = Client(api_key, api_secret, tld='us') 
    return client 

def get_price(client, ticker):
    ticker_price = client.get_symbol_ticker(symbol=ticker)
    return float(ticker_price['price'])

# might not work
def limit_buy(client, ticker, usd):
    buy_price = get_price(client, ticker)
    amount = round(usd / buy_price, 1)

    order = client.order_limit_buy(
        symbol = ticker,
        quanity = amount, 
        price = buy_price
    )
    return order

# might not work
def limit_sell(client, ticker, usd):
    sell_price = get_price(client, ticker)
    amount = round(usd / sell_price)

    order = client.order_limit_sell(
        symbol = ticker,
        quantity = amount,
        price = sell_price
    )
    return order

# useless
def trade_history(client, ticker):
    trades = client.get_my_trades(symbol=ticker)

    with open('trades.txt', 'w') as f:
        for trade in trades:
            timestamp = trade['time']
            dt = datetime.fromtimestamp(timestamp/1000)
            quantity = trade['qty']
            f.write(f'{quantity} at {dt}\n')

    return trades

def main():
    client = get_client()
    return 

if __name__ == '__main__':
    main()
