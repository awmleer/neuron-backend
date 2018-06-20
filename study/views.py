from django.http import JsonResponse, HttpResponse
from bank.models import Repo
from neuron.utils.decorator import require_login, json_request
from neuron.utils.response import ErrorResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone


@require_GET
@require_login
def generate_learn_list(request):
    amount = int(request.GET.get('amount'))
    if amount<5:
        return ErrorResponse('单词数量过少')
    elif amount>100:
        return ErrorResponse('单词数量过多')
    all_entries = Repo.objects.get(id=request.GET['repoId']).entries
    learned_entries = request.user.learned_entries
    entries = all_entries.difference(learned_entries)[:amount]
    res = []
    for entry in entries:
        res.append(entry.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def today_learned_count(request):
    count = request.user.word_records.filter(created_at__date__gte=timezone.now())
    return HttpResponse(count)
