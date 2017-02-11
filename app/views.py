from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
import django.contrib.auth as auth #用户登录认证
from app.models import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,HttpResponseForbidden
import json
from django.conf import settings
import random,string
import  urllib.request,urllib.parse
# import hashlib
from bs4 import BeautifulSoup


# Create your views here.
def repo_list(request):
    res=[]
    repos=Repo.objects.all()
    for repo in repos:
        res.append({
            'id':repo.id,
            'name':repo.name,
            'amount':repo.amount
        })
    return JsonResponse(res,safe=False)



def repo(request,repo_id):
    repo=Repo.objects.get(id=repo_id)
    res={
        'id':repo.id,
        'name':repo.name,
        'amount':repo.amount,
        'words':repo.get_words()
    }
    return JsonResponse(res)


def entry(request,word):
    e=Entry.objects.get(word=word)
    res={
        'word':e.word,
        'level':e.level,
        'definitions':e.get_definitions(),
        'phonetic':e.get_phonetic(),
        'sentences':e.get_sentences()
    }
    return JsonResponse(res)

