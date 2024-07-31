from django.urls import path
from . import views

urlpatterns = [
    path('login', view=views.login),
    path('register', view=views.register),
    path('login/google', view=views.google_login),
    path('token', view=views.validate_token),    
]
