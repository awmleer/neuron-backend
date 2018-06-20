from django.http import JsonResponse
from .models import WordRecord
from bank.models import Repo
from neuron.utils.decorator import require_login, json_request
from neuron.utils.response import ErrorResponse


@require_login
def generate_learn_list(request):
    amount = int(request.GET.get('amount'))
    if amount<5:
        return ErrorResponse('单词数量过少')
    elif amount>100:
        return ErrorResponse('单词数量过多')
    all_entries = Repo.objects.get(id=request.GET['repo_id']).entries
    learned_entries = request.user.learned_entries
    entries = all_entries.difference(learned_entries)[:amount]
    res = []
    for entry in entries:
        res.append(entry.as_dict())
    return JsonResponse(res, safe=False)


