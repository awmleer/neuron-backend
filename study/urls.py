from django.urls import path
from . import views

urlpatterns = [
    path('learn/generate-list/', views.generate_learn_list),
    path('learn/today-count/', views.today_learned_count),
    path('record/<int:record_id>/<str:mark>/', views.record_update)
]