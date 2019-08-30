from pymongo import *
import json
MONGODB_DATABASE_NAME = 'local'
MONGODB_HOST = '10.132.141.99'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'vege_sina'
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection = db[MONGODB_ARTICLE_COLLECTION]


MONGODB_DATABASE_NAME = 'Sina'
MONGODB_HOST = '10.141.212.160'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'article20190413'  # articleTest
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection_sina = db[MONGODB_ARTICLE_COLLECTION]

nlist = ['王思聪','聪聪','思聪']
raw = collection.find({"s":{'$regex' : "(.*聪聪.*)|(.*王思聪.*)"}})
vlist = ['发文嘲讽','怼','骂','怒斥','diss','挖苦','讽刺','怒怼','怒骂']
count = 0
for item in raw:
    if item['v'] in vlist:
        count += 1 
        print(item['article_id'])
        article = collection_sina.find_one({"_id":item['article_id']})
        title = article['title']
        print(title)
print(count)
