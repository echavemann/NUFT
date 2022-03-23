import pyEX as p
import pandas as pd
import os
import requests
from iexfinance.stocks import get_historical_data

api_key = 'pk_9875fe91ce264eadb369752fd783e74b'
secret = 'sk_84a2db154d084c5291a439ca156520bc'

base_url = 'https://cloud.iexapis.com/v1'
sandbox_url = 'https://sandbox.iexapis.com/stable'

df = get_historical_data("MSFT", output_format = 'pandas', token=secret)

print(df)
