from pymongo import MongoClient
class Book:
    def __init__(self, ISBN, **kwargs):
        self.ISBN = ISBN
        self.params = kwargs

book1 = Book(10086, Title = "title1", Authors = [ 'Jimsui Guan', 'James Guan'])

book1.ISBN
len(book1.params)
book1.params.get('Title')

from pymongo import MongoClient
client = MongoClient()
db = client.mongo_lib

cursor = db.books.find_one({'ISBN':"9991-1001-2002"})

set(cursor.get('Authors')) == set(['James Guan', 'Jimsui Guan'])

for (key, value) in cursor.items():
    print(key,': ', value)


for (key, value) in book1.params.items():
    if key in cursor.keys():

        if key == 'Authors':
            if set(value) != set(cursor.get('Authors')):
                print(f'Conlicting in {key}: exiting info -> {cursor.get(key)}; input -> {value}')
        else:
            if value != cursor.get(key):
            print(f'Conlicting in {key}: exiting info -> {cursor.get(key)}; input -> {value}')