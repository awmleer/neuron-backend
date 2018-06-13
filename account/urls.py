from django.urls import path
from . import views

urlpatterns = [
    path('is-logged-in/', views.is_logged_in),
    path('login/', views.login),
    path('info/', views.user_info),
    path('logout/', views.logout),
]