from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^sync/check/',views.sync_check),
    url(r'^sync/upload/',views.sync_upload),
    url(r'^sync/download/',views.sync_download),
]