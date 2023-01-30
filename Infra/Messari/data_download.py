from six.moves import urllib
import requests
import json
import csv
import pandas as pd

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-messari-api-key': '',
        'x-api-realtime-e': '',
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
