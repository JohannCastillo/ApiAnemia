from django.urls import path
from .views import send_email

urlpatterns = [
    path('send', view=send_email)       
]
