import pymongo
from pymongo import MongoClient
import alpaca_trade_api as tradeapi
import requests, json
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
from alpaca.trading import TradingClient, GetAssetsRequest


def get_time_myself(currentTime):
    return(currentTime.date().isoformat()+ 'T17:00:00Z')

API_NAME = 'PK4KNHN1288FU75AUBDI'
API_KEY = '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj'

headers = { "APCA-API-KEY-ID": "PK4KNHN1288FU75AUBDI",
    "APCA-API-SECRET-KEY": "2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj"}

# data_url = "https://paper-api.alpaca.markets"
data_url = "https://data.alpaca.markets"

tradingClient = TradingClient(API_NAME, API_KEY)
allAsset = tradingClient.get_all_assets()

# get all stock name
# symbols = [json.loads(x.json())['symbol'] for x in allAsset]
#
symbols = ['NIO','GS']
# symbols = symbols[0:15]

local_time = datetime.now(timezone.utc)
print(local_time.isoformat("T", "minutes"))

get_time_myself(local_time)

client = MongoClient()

db = client['alpacaNewsTest']
db.create_collection('test_news')
coll = db['test_news']

for symbol in symbols:
    look_back_wins = 30
    start = local_time
    for i in range(look_back_wins):
        end = start
        end_time = get_time_myself(end)
        start = (end- timedelta(days=1))
        start_time = get_time_myself(start)
        print(end_time)

        # start_time ="2022-07-10T19:00:00Z"
        # end_time = "2022-07-20T19:00:00Z"

        # start_time ="2022-07-10T19:00:00Z"
        # end_time = "2022-07-20T19:00:00Z"

        limit_num = '50'
        include_content_flag ='false'
        r = requests.get(f'{data_url}/v1beta1/news?symbols={symbol}&start={start_time}&end={end_time}&limit={limit_num}&include_content={include_content_flag}', headers = headers)
        # r = requests.get(f'{data_url}/v1beta1/news?symbols={symbols}', headers = headers)

        data = r.json()
        df = pd.json_normalize(data['news'])
        if len(df)!= 0: print(df.headline)

        # insert into database
        df.apply(lambda row: coll.insert_one(row.to_dict()), axis=1)

        time.sleep(0.5)







# temp_json = df.iloc[0].to_dict()
# json_object = json.loads(temp_json)
# json_formatted_str = json.dumps(json_object, indent=2)
# print(json_formatted_str)
# coll.insert_one(temp_json)

