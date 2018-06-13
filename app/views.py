from django.utils import timezone
from app.models import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,HttpResponseForbidden
import json
import math
from django.conf import settings
import random,string
import  urllib.request,urllib.parse
# import hashlib


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
        'words':repo.words
    }
    return JsonResponse(res)


def entry(request,word):
    e=Entry.objects.get(word=word)
    sentences=[]
    for s in e.sentences.all():
        sentences.append({
            'id':s.id,
            'text':s.text
        })
    res={
        'word':e.word,
        'level':e.level,
        'definitions':e.definitions,
        'phonetic':e.phonetic,
        'sentences':sentences
    }
    return JsonResponse(res)




@login_required
def sync_check(request):
    datas=SyncData.objects.filter(user=request.user)
    if(len(datas)==0):
        res=0
    else:
        sync_data=datas[0]
        res=math.floor(sync_data.sync_time.timestamp()*1000)
    return HttpResponse(res)



@require_http_methods(['POST'])
@login_required
def sync_upload(request):
    data = json.loads(request.body.decode())
    sync_datas=SyncData.objects.filter(user=request.user)
    if(len(sync_datas)==0):
        # create one
        sync_data=SyncData(user=request.user)
    else:
        sync_data=sync_datas[0]
    sync_data.set_data(data)
    sync_data.save()
    res=math.floor(sync_data.sync_time.timestamp()*1000)
    return HttpResponse(res)



@login_required
def sync_download(request):
    sync_data=SyncData.objects.get(user=request.user)
    return JsonResponse(sync_data.get_data())


