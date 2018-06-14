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


