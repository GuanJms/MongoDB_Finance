from pymongo import MongoClient

client = MongoClient("mongodb://433-22.csse.rose-hulman.edu:27017")

db = client['bookstore']
res = db.authors.find()
for data in res:
    print(data)