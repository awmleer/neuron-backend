from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
import django.contrib.auth as auth #用户登录认证
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
        'words':repo.get_words()
    }
    return JsonResponse(res)


def entry(request,word):
    e=Entry.objects.get(word=word)
    res={
        'word':e.word,
        'level':e.level,
        'definitions':e.definitions,
        'phonetic':e.phonetic,
        'sentences':e.sentences
    }
    return JsonResponse(res)



@require_http_methods(["POST"])
def login(request):
    data = json.loads(request.body.decode())
    user = auth.authenticate(username=data['phone'], password=data['password']) #电话号码当做username来用
    if user is not None:
        # the password verified for the user
        if user.is_active:
            # User is valid, active and authenticated
            auth.login(request, user)
            res = HttpResponse('success')
        else:
            # The password is valid, but the account has been disabled!
            res = HttpResponse('您的账号已被锁定')
    else:
        # the authentication system was unable to verify the username and password
        # The username and password were incorrect.
        res = HttpResponse('用户名或密码错误')
    return res


def logout(request):
    auth.logout(request)
    return HttpResponse('success')


def is_logged_in(request):
    # logger.info(request.user.user_info.get())
    if request.user.is_authenticated:
        return HttpResponse('true')
    else:
        return HttpResponse('false')



@require_http_methods(['GET'])
@login_required
def userinfo(request):
    user_info=request.user.user_info.get()
    res={
        'id':request.user.id,
        'phone':request.user.username,
        'name':user_info.name
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


