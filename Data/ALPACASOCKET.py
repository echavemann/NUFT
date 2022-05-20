import pandas
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL

ALPACA_API_KEY = ''
ALPACA_API_SECRET = ''

if __name__ == '__main__':
    conn = tradeapi.StreamConn(
        ALPACA_API_KEY,
        ALPACA_API_SECRET,
        base_url=URL('https://paper-api.alpaca.markets'),
        data_url=URL('https://data.alpaca.markets'),
        data_stream='alpacadatav1'
    )

    @conn.on(r'Q\..+')
    async def on_quotes(conn, channel, quote):
        print('quote', quote)
        
    conn.run('alpacadatav1/Q.GOOG')