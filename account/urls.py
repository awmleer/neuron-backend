from django.urls import path
from . import views

urlpatterns = [
    path('is-logged-in/', views.is_logged_in),
    path('login/', views.login),
    path('signup/', views.signup),
    path('profile/', views.user_profile),
    path('logout/', views.logout),
]