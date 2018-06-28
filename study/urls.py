from django.urls import path
from . import views

urlpatterns = [
    path('learn/list/', views.learn_list),
    path('learn/list/generate/', views.learn_list_generate),
    path('learn/today-count/', views.today_learned_count),
    path('review/today-count/', views.today_reviewed_count),
    path('review/list/', views.review_list),
    path('update-records/', views.update_records),
    path('sentence/<int:sentence_id>/star/', views.star_sentence),
    path('sentence/<int:sentence_id>/unstar/', views.unstar_sentence),
    path('record/<int:record_id>/toggle-tag/<str:tag>/', views.record_toggle_tag),
]