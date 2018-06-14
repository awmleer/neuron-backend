from django.urls import path
from . import views

urlpatterns = [
    path('entry/<str:word>/', views.entry),
    path('repo/list/', views.repo_list),
    path('repo/<int:repo_id>/', views.repo),
]