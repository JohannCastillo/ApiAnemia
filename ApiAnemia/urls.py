from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('api.urls')),
    path('auth/', include('auth.urls')),
    path('predict/', include('models.urls')),
]
