from django.urls import path
from . import views

urlpatterns = [
    # path('entry/<str:word>/', views.entry),
    path('learn/generate-list/', views.generate_learn_list),
]