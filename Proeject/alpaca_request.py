import alpaca.trading
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

datetime.strptime('2014-12-04', '%Y-%m-%d')

APIUSER = 'PK4KNHN1288FU75AUBDI'
APIPWD = '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj'


# keys required for stock historical data client
client = StockHistoricalDataClient('PK4KNHN1288FU75AUBDI', '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj')

# multi symbol request - single symbol is similar
multisymbol_request_params = StockBarsRequest(symbol_or_symbols = ['NIO'],
                                              start = datetime.strptime("2021-07-01", '%Y-%m-%d'),
                                              end = datetime.strptime("2021-07-05", '%Y-%m-%d'),
                                              timeframe=TimeFrame.Day)

latest_multisymbol_quotes = client.get_stock_bars(multisymbol_request_params)

latest_multisymbol_quotes.data.get('NIO')[0].json()
latest_multisymbol_quotes.data.get('NIO')[1].json()
latest_multisymbol_quotes.data.get('NIO')[2].json() # no data since 2 days data only

for i in range(len(latest_multisymbol_quotes.data.get('NIO'))):
    print(latest_multisymbol_quotes.data.get('NIO')[0])

from alpaca.trading import TradingClient, GetAssetsRequest
import json

tradingClient = TradingClient(APIUSER, APIPWD)

allAsset = tradingClient.get_all_assets()

# get all stock name
symbols = [json.loads(x.json())['symbol'] for x in allAsset]
