from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse,JsonResponse,HttpResponseBadRequest,HttpResponseForbidden
from neuron.utils.decorator import json_request, require_login
import django.contrib.auth as auth
from neuron.utils.response import ErrorResponse
from .models import User


@require_POST
@json_request
def login(request):
    user = auth.authenticate(username=request.json['username'], password=request.json['password']) #电话号码当做username来用
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


@require_GET
def logout(request):
    auth.logout(request)
    return HttpResponse()


@require_POST
@json_request
def signup(request):
    if User.objects.filter(username=request.json['username']).exists():
        return ErrorResponse('用户名已被使用')
    user = User.objects.create(
        username=request.json['username'],
        password=request.json['password'],
        nickname=request.json['nickname'],
    )
    auth.login(request, user)
    return HttpResponse()


@require_GET
def is_logged_in(request):
    # logger.info(request.user.user_info.get())
    if request.user.is_authenticated:
        return HttpResponse('true')
    else:
        return HttpResponse('false')



@require_GET
@require_login
def user_profile(request):
    return JsonResponse(request.user.as_dict())
