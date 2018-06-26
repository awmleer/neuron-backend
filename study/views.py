from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from bank.models import Repo
from neuron.utils.decorator import require_login, json_request
from neuron.utils.response import ErrorResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from .models import EntryRecord


@require_GET
@require_login
def learn_list(request):
    amount = int(request.GET.get('amount'))
    if amount<5:
        return ErrorResponse('单词数量过少')
    elif amount>100:
        return ErrorResponse('单词数量过多')
    all_entries = Repo.objects.get(id=request.GET['repoId']).entries
    records = request.user.entry_records.filter(proficiency=-1)
    res = []
    generate = request.GET.get('generate')
    records_exists = records.exists()
    if records_exists and generate is None:
        for record in records:
            res.append(record.as_dict())
    else:
        if records_exists and generate is not None:
            records.delete()
        learned_entries = request.user.learned_entries
        entries = all_entries.difference(learned_entries)[:amount]
        for entry in entries:
            record = EntryRecord(
                entry=entry,
                user=request.user
            )
            record.save()
            res.append(record.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def review_list(request):
    records = request.user.entry_records.filter(next_review_date__lte=timezone.now())
    res = []
    for record in records:
        res.append(record.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def today_learned_count(request):
    count = request.user.entry_records.filter(created_at__date__gte=timezone.now())
    return HttpResponse(count)


@require_GET
@require_login
def record_update(request, record_id, mark):
    record = request.user.entry_records.get(id=record_id)
    if mark == 'master':
        record.proficiency = 8
    elif mark == 'know':
        if record.proficiency == -1:
            record.proficiency = 6
        else:
            record.proficiency += 1
    elif mark == 'vague':
        if record.proficiency == -1:
            record.proficiency = 3
        else:
            if record.proficiency > 0:
                record.proficiency -= 1
    elif mark == 'forget':
        if record.proficiency == -1:
            record.proficiency = 0
        else:
            if record.proficiency > 2:
                record.proficiency -= 2
            else:
                record.proficiency = 0
    else:
        return HttpResponseBadRequest()
    record.flush_next_review_date()
    record.flush_updated_at()
    record.save()
    return HttpResponse()
