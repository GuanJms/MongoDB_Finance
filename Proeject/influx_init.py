import json
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from influxdb_client import InfluxDBClient

INFLUX_TOKEN = "ZANgAnyUiPQEOhK5c41fV3HKiqT7yia7qvjg5gAuEwIOyQato8LQ52dzayOPvMCBIKTWUHF2c32rFZQICmTrBw=="
INFLUX_CLOUD_URL = '127.0.0.1:8086'
BUCKET_NAME = 'MyQuant'
ORG = "RoseQuant"
# Be sure to set precision to ms, not s
QUERY_URI = 'http://{}:8086/api/v2/write?org={}&bucket={}&precision=ms'.format(INFLUX_CLOUD_URL,
                                                                               ORG, BUCKET_NAME)

headers = {'Authorization': 'Token {}'.format(INFLUX_TOKEN)}

datetime.strptime('2014-12-04', '%Y-%m-%d')
# keys required for stock historical data client
client = StockHistoricalDataClient('PK4KNHN1288FU75AUBDI',
                                   '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj')
# multi symbol request - single symbol is similar
multisymbol_request_params = StockBarsRequest(symbol_or_symbols=['NIO'],
                                              start=datetime.strptime("2021-07-01", '%Y-%m-%d'),
                                              end=datetime.strptime("2021-07-05", '%Y-%m-%d'),
                                              timeframe=TimeFrame.Minute)
latest_multisymbol_quotes = client.get_stock_bars(multisymbol_request_params)

for i in range(2):

    data_json = latest_multisymbol_quotes.data.get('NIO')[i].json()
    resp = json.loads(data_json)
    # latest_multisymbol_quotes.data.get('NIO')[1].json()
    # latest_multisymbol_quotes.data.get('NIO')[2].json() # no data since 2 days data only


    metrics = {'measurement': resp["symbol"], 'tags': {},'fields': {}}
    metrics['fields']['open'] = resp['open']
    # metrics['time'] = resp['timestamp']
    metrics['fields']['high'] = resp['high']
    metrics['fields']['low'] = resp['low']
    metrics['fields']['close'] = resp['close']
    metrics['fields']['volume'] = resp['volume']
    metrics['fields']['trade_count'] = resp['trade_count']
    metrics['fields']['vwap'] = resp['vwap']

    with InfluxDBClient(url=f"http://{INFLUX_CLOUD_URL}", token=INFLUX_TOKEN, org=ORG) as _client:

        with _client.write_api() as _write_client:
            _write_client.write(BUCKET_NAME, ORG, metrics)
            print("success")