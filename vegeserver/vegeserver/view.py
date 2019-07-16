from django.http import HttpResponse
from django.shortcuts import render
from vegeapp.models import Article

def homepage(request):
    result = Article.objects.get(id="articleID-d7971f82-38f0-4060-b065-5149a5413c8c")
    result = result.tags
    return HttpResponse(result)