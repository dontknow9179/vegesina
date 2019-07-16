from django.http import HttpResponse
from django.shortcuts import render
from vegeapp.models import Article
from elasticsearch import Elasticsearch
import json

def homepage(request):
    # result = Article.objects.get(id="articleID-d7971f82-38f0-4060-b065-5149a5413c8c")
    # result = result.tags
    # return HttpResponse(result)
    result_dict = {}
    return render(request, "index.html", result_dict)


def search(request):
    result_dict = {}
    if request.method == 'POST':
        searchinput = request.POST['searchinput']
        es = Elasticsearch(hosts='http://10.141.212.160:9200')

        action = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "title": {
                                    "query": searchinput,
                                    "boost": 1.5
                                }
                            }
                        },
                        {
                            "match": {
                                "content": ""
                            }
                        }
                    ],
                    "must": [

                    ]
                }
            },
            "size": 10,
            "_source": {
                "include": ""
            }
        }
        res = es.search(index='article20190413', doc_type='article', body=action)
        result_dict['hits'] = res["hits"]["hits"]
        result_dict['searchbar'] = searchinput
    return render(request, "index.html", result_dict)

