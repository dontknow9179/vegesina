from pymongo import *
import json
MONGODB_DATABASE_NAME = 'Sina'
MONGODB_HOST = '10.141.212.160'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'article20190413_test'
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection = db[MONGODB_ARTICLE_COLLECTION]

nlist = ['王思聪','聪聪','思聪']
raw = collection.find({"s":{"$in":nlist}})
vlist = ['发文嘲讽','怼','骂','怒斥','diss','挖苦','讽刺','怒怼']
for item in raw:
    if item['v'] in vlist:
        print(item['article_id'])

