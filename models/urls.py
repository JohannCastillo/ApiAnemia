from django.urls import path
from .views import pronostico, diagnostico, dieta, gpt
from django.urls import path, include

urlpatterns = [
    path('pronostico', view=pronostico.index),
    path('diagnostico', view=diagnostico.index),
    path('dieta', view=dieta.index),    
    path('gpt/dieta/<int:id>', view=gpt.gpt_dieta),    
    path('gpt/dietav2/<int:id>', view=gpt.gpt_dietav2),    
]
