from django.urls import path
from . import views


urlpatterns = [
    path('client/<>/', views.profile_client, name='profile_client'),
    path('trainer/<>/', views.profile_trainer, name='profile_trainer'),
]