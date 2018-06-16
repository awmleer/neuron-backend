from .models import Repo, Entry
from django.http import JsonResponse


def repo_list(request):
    res=[]
    repos=Repo.objects.all()
    for repo in repos:
        res.append(repo.as_dict())
    return JsonResponse(res, safe=False)


def repo(request,repo_id):
    r=Repo.objects.get(id=repo_id)
    res={
        'id':r.id,
        'name':r.name,
        'amount':r.amount,
        'words':r.words
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
