import requests 
import json

# defining a class for accessing the Trading API
class alp_trade:


    # class instance initialised with Base Url, Key ID and Secret Key authenticators
    # example: api = alp_trade('https://paper-api.alpaca.markets','KEY', 'SECRET')
    def __init__(self, base_url, key_id, secret_key):

        self.base_url = base_url
        self.key_id = key_id
        self.secret_key = secret_key
        self.headers = {"APCA-API-KEY-ID" : self.key_id, 'APCA-API-SECRET-KEY': self.secret_key}

    # get_account method returns account information in json format
    # example: api.get_account()
    def get_account(self):
    
        url = self.base_url + '/v2/account'
        response = requests.get(url = url, headers = self.headers)

        return response.json()
    
    # get_orders method returns by default JSON of open orders, takes as input optional 
    # list of strings query_strings 
    # example: api.get_orders(query_strings = ['status=all', 'symbols=AAPL,SBUX', 'direction=asc'])
    def get_orders(self, query_strings = None):
        
        url = self.base_url + '/v2/orders'
        url_query = self.base_url + '/v2/orders?'

        if query_strings == None:
            response = requests.get(url = url, headers = self.headers)

            return response.json()
        
        else:

            for i in range(len(query_strings)):
                url_query += query_strings[i] + "&"

            url_query.replace(url_query[-1], "")

            response = requests.get(url = url_query, headers = self.headers)

            return response.json()
    
    # request_order method places order with specific symbol, qty, notational etc
    # example: api.request_order(symbol = "SBUX", qty = "1", side= "buy", type= "market", time_in_force= "day")
    def request_order(self, symbol = None, qty = None, notational = None, side = None, type = None, time_in_force = None, 
                            limit_price = None, stop_price = None, trail_price = None, trail_percent = None):
        
        url = self.base_url + '/v2/orders'
        dict = {"symbol": symbol,
                "qty": qty, 
                "notational": notational,
                 "side": side, 
                 "type": type, 
                 "time_in_force": time_in_force,
                 "limit_price": limit_price,
                 "stop_price": stop_price,
                 "trail_price": trail_price,
                 "trail_percent": trail_percent}

        copy = {}

        for key in dict:
            if dict[key] != None:
                copy[key] = dict[key]

        post = requests.post(url = url, data = json.dumps(copy), headers= self.headers)
    
    # cancel_order method defaults to cancel all open orders, or cancel by optional id string input
    # example: api.cancel_order(id= '0123456789')
    def cancel_order(self, id = None):

        url = self.base_url + '/v2/orders'

        if id == None:
            cancel = requests.delete(url = url, headers = self.headers)
            

        else:
            url = url + "/" + id
            cancel = requests.delete(url = url, headers = self.headers)

            return print(self.get_orders(query_strings= ["status=open"]))



    # get_positions method gets all open positions, can also specify by symbol
    # example: api.get_positions(symbol= 'SBUX')
    def get_positions(self, symbol = None):

        url = self.base_url + "/v2/positions"

        if symbol == None:
            response = requests.get(url = url, headers = self.headers)

            return response.json()
        
        else: 
            url = url + "/" + symbol
            response = requests.get(url = url, headers = self.headers)

            return response.json()

    # close_positions method closes all positions, can also specify by symbol
    # example: api.close_positions(symbol= 'SBUX')
    def close_positions(self, symbol = None):

        url = self.base_url + "/v2/positions"

        if symbol == None:
            close = requests.delete(url = url, headers = self.headers)

        else:
            url = url + "/" + symbol
            close = requests.delete(url = url, headers = self.headers)
            print(close.status_code)

            return print(self.get_positions(symbol = None))

    # get_assets method gets assets by optional symbol or list of strings query_strings
    # example: api.get_assets(symbol= 'AAPL'), api.get_assets(query_strings=['status=active', 'exchange=OTC'])
    def get_assets(self, query_strings = None, symbol = None):

        url = self.base_url + "/v2/assets"
        url_query = self.base_url + "/v2/assets?"

        if symbol != None:
            url = url + "/" + symbol
            response = requests.get(url = url, headers = self.headers)

            return response.json()

        if query_strings == None:
            response = requests.get(url = url, headers = self.headers)

            return response.json()

        else:

            for i in range(len(query_strings)):
                url_query += query_strings[i] + "&"

            url_query.replace(url_query[-1], "")

            response = requests.get(url = url_query, headers = self.headers)

            return response.json()

    # get_history gets portfolio history 
    # example: api.get_history()
    def get_history(self):

        url = self.base_url + "/v2/account/portfolio/history"
        response = requests.get(url = url, headers = self.headers)

        return response.json()