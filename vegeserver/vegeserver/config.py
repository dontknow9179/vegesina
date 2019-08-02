MONGODB_DATABASE_NAME = 'Sina'
MONGODB_HOST = '10.141.212.160'
MONGODB_PORT = 27017
MONGODB_ARTICLE_COLLECTION = 'article20190413'  # articleTest
MONGODB_SESSION_COLLECTION = 'session'

ES_HOST = 'http://10.141.212.160:9200'
ES_ARTICLE_INDEX = 'article20190413'  # article20190413
ES_ARTICLE_DOC_TYPE = 'article'
ES_BULK_SIZE = 2000
# mongo到es的mapping
ES_FIELD_MAPPING = {
    "time": "date",
    "title": "title",
    "content": "content"
}
# 名字字典的位置
NAME_DICT_PATH = "HotSpotServer/component/elasticsearch/sina_actor.dic"

EXPLORE_MAX_HIT = 100
EXPLORE_CLUSTER_NUM = 4
EXPLORE_SUMMARY_MAX_LEN = 3
EXPLORE_SUMMARY_METHOD = 'centroid'  # textrank or centroid

STOPWORDS_CN = 'data/stopwords/chineseStopWords.txt'


LTP_DATA_DIR = 'EventTriplesExtraction/ltp_data_v3.4.0'
OUTPUT_PATH = 'HotSpotServer/component/event_analyze/data_path_save/1521112368/'
WORD2ID_PATH = 'HotSpotServer/component/event_analyze/data_path/word2id.pkl'
