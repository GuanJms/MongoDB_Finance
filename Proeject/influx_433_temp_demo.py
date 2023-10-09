import json
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from influxdb_client import InfluxDBClient
from datetime import datetime
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_TOKEN = 'VI8GQw6MqKWYjB8MPkd_8cTKvIsJQGAogtouSPUQXuiqATZXM9rfNeSvmMNKdvqfv_qww4qg2efGKJ2qwDzt3Q=='
ORG = "rhit"
INFLUX_CLOUD_URL = '433-25.csse.rose-hulman.edu'
BUCKET_NAME = '433db'
token = "VI8GQw6MqKWYjB8MPkd_8cTKvIsJQGAogtouSPUQXuiqATZXM9rfNeSvmMNKdvqfv_qww4qg2efGKJ2qwDzt3Q=="
org = "rhit"
bucket = "bucket-test"
# Be sure to set precision to ms, not s

import yfinance as yf
data = yf.download("MSFT", start="2021-01-01", end="2021-10-30")
# print(data.to_csv())

from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

class InfluxClient:
    def __init__(self,token,org,bucket):
        self._org=org
        self._bucket = bucket
        self._client = InfluxDBClient(url="http://433-25.csse.rose-hulman.edu:8086", token=token)

    def write_data(self, data, write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org, data, write_precision='s')

IC = InfluxClient(token,org,bucket)

# Data Write Method 2
# Data Write Method 3
IC.write_data([
{
"measurement": "MSFT",
"tags": {"stock": "MSFT"},
"fields": {
"Open": 62.79,
"High": 63.38,
"Low": 62.13,
},
"time": int(datetime.strptime('2021-11-07','%Y-%m-%d').timestamp())
},
{
"measurement": "MSFT_DATE",
"tags": {"stock": "MSFT"},
"fields": {
"Open": 62.79,
"High": 63.38,
"Low": 62.13,
},
}
],write_option=ASYNCHRONOUS)

# headers = {'Authorization': 'Token {}'.format(INFLUX_TOKEN)}
#
# datetime.strptime('2014-12-04', '%Y-%m-%d')
# # keys required for stock historical data client
# client = StockHistoricalDataClient('PK4KNHN1288FU75AUBDI',
#                                    '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj')
# # multi symbol request - single symbol is similar
# multisymbol_request_params = StockBarsRequest(symbol_or_symbols=['NIO'],
#                                               start=datetime.strptime("2021-07-01", '%Y-%m-%d'),
#                                               end=datetime.strptime("2021-07-05", '%Y-%m-%d'),
#                                               timeframe=TimeFrame.Minute)
# latest_multisymbol_quotes = client.get_stock_bars(multisymbol_request_params)
#
# for i in range(2):
#
#     data_json = latest_multisymbol_quotes.data.get('NIO')[i].json()
#     resp = json.loads(data_json)
#     # latest_multisymbol_quotes.data.get('NIO')[1].json()
#     # latest_multisymbol_quotes.data.get('NIO')[2].json() # no data since 2 days data only
#
#     metrics = {'measurement': resp["symbol"], 'tags': {},'fields': {}}
#     metrics['fields']['open'] = resp['open']
#     # metrics['time'] = resp['timestamp']
#     metrics['fields']['high'] = resp['high']
#     metrics['fields']['low'] = resp['low']
#     metrics['fields']['close'] = resp['close']
#     metrics['fields']['volume'] = resp['volume']
#     metrics['fields']['trade_count'] = resp['trade_count']
#     metrics['fields']['vwap'] = resp['vwap']
#
#     with InfluxDBClient(url="http://433-25.csse.rose-hulman.edu:8086", token=token, org=org) as _client:
#
#         with _client.write_api() as _write_client:
#             _write_client.write(BUCKET_NAME, org, metrics)
#             print("success")