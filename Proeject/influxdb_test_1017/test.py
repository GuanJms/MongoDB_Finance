import json
from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
bucket = "bucket-test"
org = "organization-test"
token = "fCD_yfLk_iDUPe52t3Zvel8c8d8PFEKPY7uyvcofi4mPPiBb9yp5sba0j0nP73pVgrE6Y6tLTyLW701OPqCnow=="

def load_stock_data_API(stock, start_time, stop_time, time_frame=TimeFrame.Day):
    our_client = StockHistoricalDataClient('PK4KNHN1288FU75AUBDI',
                                           '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj')
    # multi symbol request - single symbol is similar
    request_data = StockBarsRequest(symbol_or_symbols=[stock],
                                    start=start_time,
                                    end=stop_time,
                                    timeframe=time_frame)
    data_bar = our_client.get_stock_bars(request_data)
    # print(len(data_bar.data.get(stock)))

    batch_number = 50
    for i in range(0, len(data_bar.data.get(stock)), batch_number):
        rows = []
        if i + batch_number > len(data_bar.data.get(stock)):
            batch_number = len(data_bar.data.get(stock)) - i

        for k in range(batch_number):
            row = data_bar.data.get(stock)[i+k].dict()
            date, symbol, open, high, low, close, volume, trade_count, vwap = row["timestamp"], row['symbol'], row[
                "open"], row["high"], row["low"], row["close"], row["volume"], row["trade_count"], row["vwap"]
            line_protocol_string = ''
            line_protocol_string += f'stock_{symbol},'
            line_protocol_string += f'stock={symbol} '
            line_protocol_string += f'Open={open},High={high},Low={low},Close={close},' \
                                    f'Volume={volume},Trade_count={trade_count},Vwap={vwap} '
            line_protocol_string += str(int(date.timestamp()))
            rows.append(line_protocol_string)
        print(len(rows))


load_stock_data_API(stock='NIO', start_time=datetime.strptime("2021-10-19", '%Y-%m-%d'),
                       stop_time=datetime.strptime("2022-10-19", '%Y-%m-%d'))