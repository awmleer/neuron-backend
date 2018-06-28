from django.core.paginator import Paginator


def generatePage(queryset, page_number, page_size, handler):
    ret = {}
    ret['items'] = []
    paginator = Paginator(queryset, page_size)
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
    items = paginator.page(page_number).object_list
    ret['next'] = page_number < paginator.num_pages
    ret['items'] = [handler(item) for item in items]
    return ret

