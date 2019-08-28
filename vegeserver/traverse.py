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
collection_new = db['article20190413_test']

articles = collection.find({})
for article in articles:
    try:

        svos = extractor.triples_main_vege(article['title'],article['_id'])
        if len(svos) > 0:
            collection_new.insert_many(svos)
    except Exception as e:
        print('Reason:', e)
        print(article['_id'])