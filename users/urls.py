from django.urls import path
from . import views


urlpatterns = [
    path('client/<str:username>/', views.profile_client, name='profile_client'),
    path('trainer/<str:username>/', views.profile_trainer, name='profile_trainer'),
    path('', views.index, name="index")
]