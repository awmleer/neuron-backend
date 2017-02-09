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
def pa(request):
    result=urllib.request.urlopen("http://dict.cn/%s"%urllib.request.quote('more')).read()
    soup=BeautifulSoup(result)
    # print(result)
    # items=soup.select('.s-item-container')
    definitions=soup.select('.dict-basic-ul li')
    phonetics=soup.select('.word .phonetic span')
    res={
        'word':soup.select('.word-cont .keyword')[0].get_text(strip=True),
        'level':soup.select('.word-cont a')[1].get('class')[0].replace('level_','',1),
        'phonetic':{
            'UK':{
                'symbol':phonetics[0].select('bdo')[0].get_text(),
                'sound':{
                    'female':phonetics[0].select('i.sound')[0].get('naudio'),
                    'male':phonetics[0].select('i.sound')[1].get('naudio')
                }
            },
            'US':{
                'symbol':phonetics[1].select('bdo')[0].get_text(),
                'sound':{
                    'female':phonetics[1].select('i.sound')[0].get('naudio'),
                    'male':phonetics[1].select('i.sound')[1].get('naudio')
                }
            }
        },
        # 'syllable':soup.select('.word-cont .keyword')[0].get('tip').replace('音节划分：','',1),
        'definitions':[],
        'examples':[]
    }
    for definition in definitions:
        if definition.get('style') is not None: continue
        # print(definition.get('style'))
        res['definitions'].append({
            'type':definition.select('span')[0].get_text(),
            'text':definition.select('strong')[0].get_text()
        })
    examples=soup.select('.section.sent .layout.sort')[0]
    groups=examples.select('div b')
    count=0
    for group in groups:
        group={
            'type':group.get_text(),
            'sentences':[]
        }
        sentences=examples.select('ol')[count].select('li')
        count+=1
        for sentence in sentences:
            i_tags=sentence.select('i')
            for i_tag in i_tags:
                i_tag.decompose()
            group['sentences'].append(sentence.prettify().replace('\n ','').replace('</em>','</em> ').replace('<em class=\"hot\"> ',' <em class=\"hot\">').replace('\n','').replace('<li>','').replace('</li>',''))
        res['examples'].append(group)


    return JsonResponse(res)