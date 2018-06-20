import json
from django.http import HttpResponse


def json_request(viewFunction):
    def _wrapped(request, *args, **kwargs):
        if request.method=='POST':
            request.json = json.loads(request.body.decode())
        return viewFunction(request, *args, **kwargs)
    return _wrapped


def require_login(func):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return func(request, *args, **kwargs)
    return inner