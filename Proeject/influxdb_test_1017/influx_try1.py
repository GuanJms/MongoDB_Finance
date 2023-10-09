from datetime import datetime
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
bucket = "bucket-test"
org = "organization-test"
token = "fCD_yfLk_iDUPe52t3Zvel8c8d8PFEKPY7uyvcofi4mPPiBb9yp5sba0j0nP73pVgrE6Y6tLTyLW701OPqCnow=="

client = InfluxDBClient(url="http://localhost:8086", token=token)

import yfinance as yf
data = yf.download("MSFT", start="2021-01-01", end="2021-10-30")
# print(data.to_csv())
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS


class InfluxClient:
    def __init__(self,token,org,bucket):
        self._org=org
        self._bucket = bucket
        self._client = InfluxDBClient(url="http://localhost:8086", token=token)


    def write_data(self, data, write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org, data, write_precision='s')


IC = InfluxClient(token,org,bucket)
# Data Write Method 1
IC.write_data(["MSFT,stock=MSFT Open=62.79,High=63.84,Low=62.13"])

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