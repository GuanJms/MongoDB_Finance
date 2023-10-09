from pymongo import MongoClient
import yfinance as yf
from datetime import datetime
import pandas as pd

ticker_symbols = ["SPY","ERIE"]
data_monthly = yf.download(ticker_symbols, start= datetime.strptime("2023-05-01", "%Y-%m-%d"),interval='1d')

# client = MongoClient()
#
# db = client['stockDataTest']
# db.create_collection('test_stock')
# coll = db['test_stock']

print(data_monthly.iloc[])