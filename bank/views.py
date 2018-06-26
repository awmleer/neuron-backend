from .models import Repo, Entry
from django.http import JsonResponse, HttpResponse
from neuron.utils.decorator import require_login
from django.views.decorators.http import require_GET


@require_GET
def repo_list(request):
    res=[]
    repos=Repo.objects.all()
    for r in repos:
        res.append(r.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
def repo(request,repo_id):
    r=Repo.objects.get(id=repo_id)
    return JsonResponse(r.as_dict())


@require_GET
@require_login
def entry(request,word):
    e=Entry.objects.get(word=word)
    return JsonResponse(e.as_dict())

