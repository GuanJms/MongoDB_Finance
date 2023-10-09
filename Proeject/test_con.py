from pymongo import MongoClient
import urllib

# cars = [{'name': 'Audi', 'price': 52642},
#         {'name': 'Mercedes', 'price': 57127}, {'name': 'Skoda', 'price': 9000}, {'name': 'Volvo', 'price': 29000},
#         {'name': 'Bentley', 'price': 350000}, {'name': 'Citroen', 'price': 21000}, {'name': 'Hummer', 'price': 41400},
#         {'name': 'Volkswagen', 'price': 21600}]

mongo_uri = "mongodb://admin:didisucks@137.112.104.222:27017/test"
client = MongoClient(mongo_uri)

# client = MongoClient('mongodb://137.112.104.222:27017')

db = client["test"]

cursor = db["user"].find()

for data in cursor:
    print(data)

#
# import pymongo
# from sshtunnel import SSHTunnelForwarder
#
#
# with SSHTunnelForwarder(
#     '433-22.csse.rose-hulman.edu',
#     ssh_username='csse',
#     ssh_password='Vu3cheik',
#     remote_bind_address=('127.0.0.1', 27017),
#     local_bind_address=('0.0.0.0', 10022)
# ) as server:
#
#     print(server.ssh_host)
#     print(server.ssh_port)
#     print(server.local_bind_ports)
#     print(server.tunnel_is_up)
#
#     print("here")
#
#     client = pymongo.MongoClient(host = '0.0.0.0', port=10022)
#
#
#     db = client['test-database']
#     collection = db.test_collection
#     post = {"author": "Mike",
#             "text": "My first blog post!",
#             "tags": ["mongodb", "python", "pymongo"]}
#
#     posts = db.posts
#     post_id = posts.insert_one(post).inserted_id
#     post_id
#
#
#     server.close()
#



# import redis
# from sshtunnel import SSHTunnelForwarder
#
#
# with SSHTunnelForwarder(
#     '433-22.csse.rose-hulman.edu',
#     ssh_username='csse',
#     ssh_password='Vu3cheik',
#     remote_bind_address=('127.0.0.1', 6379),
#     local_bind_address=('0.0.0.0', 10022)
# ) as server:
#
#     print(server.ssh_host)
#     print(server.ssh_port)
#     print(server.local_bind_ports)
#     print(server.tunnel_is_up)
#
#     print("here")
#     red = redis.Redis(host = '0.0.0.0', port=10022, decode_responses=True)
#     print(red.ping())
#
#     red.flushdb()
#     red.set("hh", "pp")
#     red.set('ss', 'dd')
#     result = red.get("hh")
#     # red.flushdb()
#     print(result)
#
#     server.close()
#

x = ['a','a']
x.remove('a')

