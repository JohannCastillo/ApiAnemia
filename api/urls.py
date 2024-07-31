from django.urls import path
from .views import paciente, diagnostico, apoderado, ubigeos;

urlpatterns = [
    # Pacientes
    path('pacientes', view=paciente.index),
    path('pacientes/<int:id>', view=paciente.get_paciente_by_id),
    path('pacientes/apoderado/<int:apoderado_id>', view=paciente.get_pacientes_by_apoderado),
    path('pacientes/apoderado/<int:apoderado_id>/create', view=paciente.create),

    # Diagnósticos
    path('diagnosticos', view=diagnostico.index),

    # Apoderados
    path('apoderados', view=apoderado.index),
    path('apoderados/<int:id>', view=apoderado.get_apoderado_by_id),
    path('apoderados/usuario/<int:user_id>', view=apoderado.get_apoderado_by_user_id),
    path('apoderados/create', view=apoderado.create),
    path('apoderados/<int:id>/update', view=apoderado.update),

    # Ubigeos
    path('ubigeos', view=ubigeos.index),
    path('provincias', view=ubigeos.provincias),
    path('departamentos', view=ubigeos.departamentos),
    path('distritos', view=ubigeos.distritos),
    path('distritos/provincia/<int:provincia_id>', view=ubigeos.get_distrito_by_provincia_id),
]
