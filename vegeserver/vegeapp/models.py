from django.db import models

# Create your models here.
from mongoengine import Document, EmbeddedDocument
import datetime
from mongoengine.fields import *
import vegeserver.config as config


class Article(Document):
    # Meta variables.
    meta = {
        'collection': config.MONGODB_ARTICLE_COLLECTION
    }

    # Document variables.
    id = StringField(primary_key=True)
    time = StringField()
    types = ListField(StringField(), default=list)
    tags = ListField(StringField(), default=list)
    source = StringField()
    channel = StringField()
    title = StringField()
    url = StringField()
    code = StringField()
    content = StringField()
    imgUrls = ListField(StringField(), default=list)

