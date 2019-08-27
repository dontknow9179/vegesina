from pymongo import *
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
collection_new = db['article20190413_test']
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
    "from": 10,
    "size": 10,
    "_source": {
        "include": ""
    }
}

res = es.search(index='article20190413', doc_type='article', body=action)
# svos = extractor.triples_main_vege("王思聪新女友想靠王思聪上位，王思聪怒怼现任女友？") 
# print(svos)
for item in res["hits"]["hits"]:
    article = collection.find_one({"_id":item['_id']})
    title = article['title']
    print(title)
    svos = extractor.triples_main_vege(title,article['_id']) 
    print(svos)   
    content = article['content']
    print(content)
    svos += extractor.triples_main_vege(content,article['_id'],sentence_count=4)
    print(svos)
    # if len(svos) > 0:
    #     collection_new.insert_many(svos)
# collection_new.insert_many([{'s': '思聪', 'v': '怒怼', 'o': '女友'}, {'s': '思聪', 'v': '怒怼', 'o': '女友'}, {'s': '网传', 'v': '是', 'o': '女孩'}, {'s': '网传', 'v': '是', 'o': '女孩'}, {'s': '女孩', 'v': '酷似', 'o': '幂'}, {'s': '她', 'v': '删', 'o': '微博'}, {'s': '她', 'v': '删', 'o': '微博'}, {'s': '她', 'v': '删', 'o': '微博'}, {'s': '她', 'v': '删', 'o': '微博'}, {'s': '她', 'v': '删', 'o': '微博'}, {'s': '女孩', 'v': '想', 'o': '上位'}])
  

