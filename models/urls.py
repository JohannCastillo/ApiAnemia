from django.urls import path
from .views import pronostico, diagnostico, dieta

urlpatterns = [
    path('pronostico', view=pronostico.index),
    path('diagnostico', view=diagnostico.index),
    path('dieta', view=dieta.index),    
]
