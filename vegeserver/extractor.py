from pymongo import MongoClient
from elasticsearch import Elasticsearch
import json
from triple_extract.triple_extract import *

MONGODB_DATABASE_NAME = 'Sina'
MONGODB_HOST = '10.141.212.160'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'article20190413'  # articleTest
conn = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[MONGODB_DATABASE_NAME]
collection = db[MONGODB_ARTICLE_COLLECTION]
es = Elasticsearch(hosts='http://10.141.212.160:9200')

action = {
    "query": {
        "bool": {
            "should": [
                {
                    "match": {
                        "title": {
                            "query": "王思聪",
                            "boost": 1.5
                        }
                    }
                },
                {
                    "match": {
                        "content": "王思聪"
                    }
                }
            ]    
        }
    },
    "size": 10,
    # "_source": {
    #     "include": ""
    # }
}
res = es.search(index='article20190413', doc_type='article', body=action)

for item in res["hits"]["hits"]:
    # print(item['_id'])
    # print(item['_source']['title'])
    # print(item['_source']['content'])
    article = collection.find_one({"_id":item['_id']})
    title = article['title']
    print(title)
    svos = extractor.triples_main_vege(title)    
    content = article['content']
    print(content)
    svos += extractor.triples_main_vege(content,sentence_count=4)
    print(svos)
    

