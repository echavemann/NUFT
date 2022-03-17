import requests
import pandas as pd
import json
import numpy
API_KEY = ''

res = requests.get('https://api.glassnode.com/v1/metrics/indicators/sopr',
    params={'a': 'BTC', 'api_key': API_KEY})
