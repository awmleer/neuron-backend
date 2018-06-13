from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,HttpResponseForbidden
from neuron.utils.decorator import json_request
import django.contrib.auth as auth
from neuron.utils.response import ErrorResponse


@json_request
@require_http_methods(["POST"])
def login(request):
    user = auth.authenticate(username=request.json['phone'], password=request.json['password']) #电话号码当做username来用
    if user is not None:
        # the password verified for the user
        if user.is_active:
            # User is valid, active and authenticated
            auth.login(request, user)
            res = HttpResponse()
        else:
            # The password is valid, but the account has been disabled!
            res = ErrorResponse('您的账号已被锁定')
    else:
        # the authentication system was unable to verify the username and password
        # The username and password were incorrect.
        res = ErrorResponse('用户名或密码错误')
    return res


@require_http_methods(["GET"])
def logout(request):
    auth.logout(request)
    return HttpResponse()


@require_http_methods(["GET"])
def is_logged_in(request):
    # logger.info(request.user.user_info.get())
    if request.user.is_authenticated:
        return HttpResponse('true')
    else:
        return HttpResponse('false')



@require_http_methods(['GET'])
@login_required
def user_info(request):
    return JsonResponse(request.user.as_dict())
