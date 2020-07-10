from django.urls import path
from . import views

urlpatterns = [
    path("singup/", views.signup_choice, name="signup_choice"),
    path("signup/<str:signup_type>/", views.signup, name="signup_main")
]