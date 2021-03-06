from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from bank.models import Repo, Sentence
from neuron.utils.decorator import require_login, json_request
from neuron.utils.response import ErrorResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from .models import EntryRecord
from neuron.utils.pagination import generatePage
import datetime


@require_GET
@require_login
def learn_list(request):
    records = request.user.entry_records.filter(proficiency=-1).select_related('entry')
    res = []
    for record in records:
        res.append(record.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def learn_list_generate(request):
    amount = int(request.GET.get('amount'))
    if amount < 5:
        return ErrorResponse('单词数量过少')
    elif amount > 100:
        return ErrorResponse('单词数量过多')
    all_entries = Repo.objects.get(id=request.GET['repoId']).entries.all()
    request.user.entry_records.filter(proficiency=-1).delete()
    res = []
    learned_entries = request.user.learned_entries.all()
    entries = all_entries.difference(learned_entries).all()[:amount]
    for entry in entries:
        record = EntryRecord(entry=entry, user=request.user)
        record.save()
        res.append(record.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def review_list(request):
    records = request.user.entry_records.filter(next_review_date__lte=timezone.now()).select_related('entry')
    res = []
    for record in records:
        res.append(record.as_dict())
    return JsonResponse(res, safe=False)


@require_GET
@require_login
def today_learned_count(request):
    count = request.user.entry_records.filter(learned_at__date=datetime.date.today()).count()
    return HttpResponse(count)


@require_GET
@require_login
def today_reviewed_count(request):
    today = timezone.now().date()
    count = request.user.entry_records.filter(updated_at__date__gte=today).filter(learned_at__date__lt=today).count()
    return HttpResponse(count)


@require_POST
@require_login
@json_request
def update_records(request):
    for item in request.json:
        record = request.user.entry_records.get(id=item['id'])
        mark = item['mark']
        if record.proficiency != -1 and record.next_review_date > datetime.date.today():
            continue
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
            mark = None
        if mark is not None:
            if record.learned_at is None:
                record.learned_at = timezone.now()
            record.flush_next_review_date()
            record.flush_updated_at()
            record.save()
    return HttpResponse()


@require_GET
@require_login
def star_sentence(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    record = EntryRecord.objects.get(entry_id=sentence.entry_id, user=request.user)
    if sentence_id not in record.starred_sentence_ids:
        record.starred_sentence_ids.append(sentence_id)
        record.save()
    return JsonResponse(record.starred_sentence_ids, safe=False)


@require_GET
@require_login
def unstar_sentence(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    record = EntryRecord.objects.get(entry_id=sentence.entry_id, user=request.user)
    if sentence_id in record.starred_sentence_ids:
        record.starred_sentence_ids.remove(sentence_id)
        record.save()
    return JsonResponse(record.starred_sentence_ids, safe=False)


@require_GET
@require_login
def record_toggle_tag(request, record_id, tag):
    record = request.user.entry_records.get(id=record_id)
    if tag in record.tags:
        record.tags.remove(tag)
    else:
        record.tags.append(tag)
    record.save()
    return JsonResponse(record.tags, safe=False)


@require_GET
@require_login
def record_list(request, page_number):
    records = request.user.entry_records.filter(proficiency__gte=0).select_related('entry')
    page = generatePage(records, page_number, 20, lambda r:r.as_dict())
    return JsonResponse(page)
