from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^entry/(?P<word>.+)/$',views.entry),
    url(r'^repo/list/$',views.repo_list),
    url(r'^repo/(?P<repo_id>[0-9]+)/$',views.repo),
    url(r'^account/is_logged_in/',views.is_logged_in),
    url(r'^account/login/',views.login),
    url(r'^account/userinfo/',views.userinfo),
    url(r'^account/logout/',views.logout),
    url(r'^sync/check/',views.sync_check),
    url(r'^sync/upload/',views.sync_upload),
    url(r'^sync/download/',views.sync_download),
]