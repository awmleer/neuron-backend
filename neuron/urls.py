from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('bank/', include('bank.urls')),
    path('study/', include('study.urls')),
]
