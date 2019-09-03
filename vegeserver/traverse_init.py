from pymongo import *
import json
from triple_extract.triple_extract import *

MONGODB_DATABASE_NAME = 'Sina'
MONGODB_HOST = '10.141.212.160'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'article20190413'  # articleTest
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection = db[MONGODB_ARTICLE_COLLECTION]

MONGODB_DATABASE_NAME = 'local'
MONGODB_HOST = '10.132.141.99'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'vege_sina'  # articleTest
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection_to = db[MONGODB_ARTICLE_COLLECTION]

articles = collection.find({})
count = 0
for article in articles:
    try:
        svos = extractor.triples_main_vege(article['content'],article['_id'],2)
        if len(svos) > 0:
            collection_to.insert_many(svos)
            count += 1
            if count % 100 == 0:
                print(count) 
    except Exception as e:
        print('Reason:', e)
        print(article['_id'])
        print(count)