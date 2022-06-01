from ast import literal_eval

from pymongo import MongoClient

con_link = 'mongodb://localhost:27017/'
cluster = MongoClient(con_link)
db = cluster['metabomb']
collection_1 = db['contract_transactions']


res = list(collection_1.find({"hash": "0xc0000fadb147fe589523d7d3648620fb171185a08689794c5acab5389103ebf3"}))[0]

print(res['input'])
print(res['input'][10:74])
# print(literal_eval(res['input'][10:75]))
# print(literal_eval('8e9dff9d58e6da4ab5017566b73749bf98ce53c741d1b9e7732f2e63c9f993da'))
print(int('000000000000000000000000000000000000000000000000000000000000000a', 16))