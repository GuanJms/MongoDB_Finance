from sshtunnel import SSHTunnelForwarder
import pymongo
import pprint

MONGO_HOST = "433-22.csse.rose-hulman.edu"
MONGO_DB = "db"
MONGO_USER = "csse"
MONGO_PASS = "Vu3cheik"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('137.112.104.222', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
collection = db['testCollection']
collection1 = db['testCollection1']

db.list_collection_names()
collection.find()

pprint.pprint(collection.find_one())

server.stop()