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
            'repo_id':repo.id,
            'name':repo.name
        })
    return JsonResponse(res,safe=False)



def repo(request,repo_id):
    repo=Repo.objects.get(id=repo_id)
    res={
        'repo_id':repo.id,
        'name':repo.name,
        'words':repo.get_words()
    }
    return JsonResponse(res)