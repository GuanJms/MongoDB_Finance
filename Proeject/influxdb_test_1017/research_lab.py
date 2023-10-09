from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import time

bucket = "research"
org = "organization-test"
token = "fCD_yfLk_iDUPe52t3Zvel8c8d8PFEKPY7uyvcofi4mPPiBb9yp5sba0j0nP73pVgrE6Y6tLTyLW701OPqCnow=="


class InfluxClient:

    def __init__(self, token, org, bucket):
        self._org = org
        self._bucket = bucket
        self._client = InfluxDBClient(url="http://localhost:8086", token=token)

    def write_data(self, data, write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        #         write_api.write(self._bucket, self._org, data, write_precision='s')
        write_api.write(self._bucket, self._org, data)

    def add(self, userID, orderID, stock_item, num_stock, buy_or_sell, status='RUN', time_input=None):
        order = {'measurement': userID, 'tags': {}, 'fields': {}}
        if time_input is not None:
            order['time'] = int(time_input.timestamp()*10**9)
        #             print(order['time'])
        order['tags']['orderID_tag'] = orderID
        order['fields']['orderID'] = orderID
        order['fields']['status'] = status
        order['fields']['stock_item'] = stock_item
        order['fields']['num_stock'] = num_stock
        order['fields']['buy_or_sell'] = buy_or_sell
        self.write_data(order)

    def update_status(self, userID, orderID, new_status, time_input):
        order = {'measurement': userID, 'tags': {}, 'fields': {}, 'time': time_input}
        order['tags']['orderID_tag'] = orderID
        order['fields']['orderID'] = orderID
        order['tags']['status_tag'] = new_status
        order['fields']['status'] = new_status
        self.write_data(order)

    def search_userID(self, userID, start="1970-01-01", range_time=None):
        start_time_int = int(datetime.strptime(start, '%Y-%m-%d').timestamp())
        if range_time is not None:
            start_time_int = range_time
        query_client = self._client.query_api()
        #         query_input = f'from(bucket: "research")\
        #                 |> range(start: {start})\
        #                 |> filter(fn: (r) => r._measurement == "{ID}")'
        #         result = self.query_data(query_input)

        query_input = f'from(bucket:"{self._bucket}")\
                                           |> range(start: {start_time_int}) \
                                           |> filter(fn: (r) => r["_measurement"] == "{userID}")\
                                           |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
                                           |> keep(columns: ["_measurement","_time","orderID","stock_item", "num_stock", "status", "buy_or_sell"])'
        data_frame = query_client.query_data_frame(org=self._org, query=query_input)
        # print(data_frame.to_string())
        return data_frame

    def delete_user(self, measurement, start="1870-01-01T00:00:00Z", stop="2023-10-30T00:00:00Z"):
        delete_api = self._client.delete_api()
        delete_api.delete(start, stop, f'_measurement="{measurement}"', bucket=self._bucket, org=self._org)

    def delete_order(self, userID, orderID, start="1970-01-01T00:00:00Z", stop="2023-10-30T00:00:00Z"):
        delete_api = self._client.delete_api()
        delete_api.delete(start, stop, f'_measurement="{userID}" AND orderID_tag ="{orderID}"', bucket=self._bucket,
                          org=self._org)

    def search_order(self, orderID, start="1970-01-01"):
        start_time_int = int(datetime.strptime(start, '%Y-%m-%d').timestamp())
        query_client = self._client.query_api()

        query_input = f'from(bucket:"{self._bucket}")\
                                           |> range(start: {start_time_int}) \
                                           |> filter(fn: (r) => r["orderID_tag"] == "{orderID}")\
                                           |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
                                           |> keep(columns: ["_measurement","_time","orderID","stock_item", "num_stock", "status", "buy_or_sell"])'
        data_frame = query_client.query_data_frame(org=self._org, query=query_input)
        # print(data_frame.to_string())
        return data_frame

    def search_status(self, status, start="1970-01-01"):
        start_time_int = int(datetime.strptime(start, '%Y-%m-%d').timestamp())
        query_client = self._client.query_api()
        query_input = f'from(bucket:"{self._bucket}")\
                                           |> range(start: {start_time_int}) \
                                           |> filter(fn: (r) => r.status_tag == "{status}")\
                                           |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
                                           |> keep(columns: ["_time", "orderID_tag", "status_tag"])'
        data_frame = query_client.query_data_frame(org=self._org, query=query_input)
        # print(data_frame.to_string())
        return data_frame

    def search_item(self, item):
        self.write_data()

    def search_buy_or_sell(self, status):
        self.write_data()

    def query_data(self, query):
        query_api = self._client.query_api()
        result = query_api.query(org=self._org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value(), record.get_field()))
        #         print(results)
        return results


def begin(client):
    welcome = "Welcome!!!This is just a simple app for market order!!!\nPlease enter the command:\n" \
              "add order / update status / delete order / search order / get order by ID\n"
    msg = input(welcome)
    if msg.split()[0] == "add":
        question = "To add a new order, please input UserID, OrderID, item name, number of items, buy/sell ( use , to seperate)"
        data = input(question)
        inputs = data.split(',')
        client.add(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4])
    elif msg.split()[0] == "update":
        client.update_status()


    elif msg.split()[0] == "delete":

        client.delete_order()


    elif msg.split()[0] == "search":
        client.search_item()


    elif msg.split()[0] == "get":
        question = "Input order ID"
        data = input(question)
        print(f"Order {data}", client.search_userID(data))
    else:
        print("invalid input!!!")
        return