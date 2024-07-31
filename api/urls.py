from django.urls import path
from .views import paciente;

urlpatterns = [
    # Pacientes
    path('pacientes', view=paciente.index),
    path('pacientes/<int:apoderado_id>', view=paciente.get_pacientes_by_apodeado),
    path('pacientes/<int:apoderado_id>/create', view=paciente.create),
]
