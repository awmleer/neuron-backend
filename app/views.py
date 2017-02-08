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
    definitions=soup.select('.dict-basic-ul')
    res={
        'word':soup.select('.word-cont .keyword')[0].get_text(strip=True),
        'level':soup.select('.word-cont a')[1].get('class')[0].replace('level_','',1),
        # 'syllable':soup.select('.word-cont .keyword')[0].get('tip').replace('音节划分：','',1),
        'definitions':[],
        'examples':[]
    }
    for definition in definitions:
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
    # for item in items:
    #     res.append({
    #         'title':item.select('.s-access-title')[0].get_text(strip=True),
    #         'links':{
    #             # 'douban':item.select('.info h2 a')[0].get('href')
    #             'amazon':item.select('.s-access-detail-page')[0].get('href')
    #         },
    #         'pic_src':item.select('img')[0].get('src'),
    #         # 'pic_src':item.select('.pic .nbg img')[0].get('src'),
    #         'author':item.contents[2].select('span')[-1].get_text(),
    #         'pub_time':item.select('> div:nth-of-type(3) > div:nth-of-type(1) span')[-1].get_text(),
    #         # 'pub':item.select('.pub')[0].get_text(strip=True),
    #         # 'rating':item.select('.info .star .rating_nums')[0].get_text(strip=True) if len(item.select('.info .star .rating_nums'))>0 else 'N/A',
    #         'rating':item.select('div')[-1].select('span')[-1].get_text()
    #     })
    return JsonResponse(res)