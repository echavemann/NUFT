from six.moves import urllib
import requests
import json
import csv
import pandas as pd

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-messari-api-key': '859c4662-d48c-4e8b-9597-a185e4b435d8',
        'x-api-realtime-e': 'eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.XmuAS3x5r-0MJuwLDdD4jNC6zjsY7HAFNo2VdvGg6jGcj4hZ4NaJgH20ez313H8An9UJrsUj8ERH0R8UyjQu2UGMUnJ5B1ooXFPla0LQEbN_Em3-IG84YPFcWVmEgcs1Fl2jjlKHVqZp04D21UvtgQ4xyPwQ-QDdTxHqyvSCpcE.ACRnQsNuTh1K_C9R.xpLNZ8Cc9faKoOYhss1CD0A4hG4m0M7-LZQ0fISw7NUHwzQs2AEo9ZXfwOvAj1fCbcE96mbKQo8gr7Oq1a2-piYXM1X5yNMcCxEaYyGinpnf6PGqbdr6zbYZdqyJk0KrxWVhKSQchLJaLGJOts4GlpqujSqJObJQcWWbkJQYKG9K7oKsdtMAKsHIVo5-0BCUbjKVnHJNsYwTsI7xn2Om8zGm4A.nBOuiEDssVFHC_N68tDjVA',
    }
url = "https://data.messari.io/api/v1/assets"
data = requests.get(url, headers=headers).json()
# save data in json file
with open('data.json', 'w') as f:
    json.dump(data, f)
# now convert the json file to csv with the same headers as the json file
data = json.load(open('data.json'))
df = pd.DataFrame(data['data'])
df = df[['symbol', 'name', 'slug', 'metrics', 'id']]
df.to_csv('data.csv', index=False)