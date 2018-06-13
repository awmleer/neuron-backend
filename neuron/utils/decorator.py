import json

def json_request(viewFunction):
    def _wrapped(request, *args, **kwargs):
        if request.method=='POST':
            request.json = json.loads(request.body.decode())
        return viewFunction(request, *args, **kwargs)
    return _wrapped
