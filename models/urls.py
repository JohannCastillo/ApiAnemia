from django.urls import path
from .views import pronostico, diagnostico, dieta
from django.urls import path, include

urlpatterns = [
    path('pronostico', view=pronostico.index),
    path('diagnostico', view=diagnostico.index),
    path('dieta', view=dieta.index),    
]
