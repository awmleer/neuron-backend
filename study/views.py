from django.http import JsonResponse
from .models import WordRecord
from bank.models import Repo
from neuron.utils.decorator import require_login, json_request


@require_login
def generate_learn_list(request):
    all_entries = Repo.objects.get(id=request.GET['repo_id']).entries
    learned_entries = request.user.learned_entries
    entries = all_entries.difference(learned_entries)
    res = []
    for entry in entries:
        res.append(entry.as_dict())
    return JsonResponse(res, safe=False)


