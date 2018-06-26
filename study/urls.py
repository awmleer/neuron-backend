from django.urls import path
from . import views

urlpatterns = [
    path('learn/list/', views.learn_list),
    path('learn/list/generate/', views.learn_list_generate),
    path('learn/today-count/', views.today_learned_count),
    path('review/list/', views.review_list),
    path('record/<int:record_id>/<str:mark>/', views.record_update),
]