from django.urls import path

from api.views import dieta
from .views import paciente, diagnostico, apoderado, ubigeos;

urlpatterns = [
    # Pacientes
    path('pacientes', view=paciente.index),
    path('pacientes/<int:id>', view=paciente.get_paciente_by_id),
    path('pacientes/dni/<int:dni>', view=paciente.get_paciente_by_dni),
    path('pacientes/cnv/<int:cnv>', view=paciente.get_paciente_by_cnv),
    path('pacientes/apoderado/user/create', view=paciente.create_by_user),
    path('pacientes/apoderado/<int:apoderado_id>', view=paciente.get_pacientes_by_apoderado),
    path('pacientes/apoderado/<int:apoderado_id>/create', view=paciente.create),

    # Niveles de anemia
    path('niveles-anemia', view=diagnostico.niveles_anemia),

    # Diagnósticos
    path('diagnosticos', view=diagnostico.index),
    path('diagnosticos/estadisticas/paciente/<int:id_paciente>', view=diagnostico.estadisticas_por_paciente_id),
    path('diagnosticos/estadisticas/evolucion-mensual', view=diagnostico.estadisticas_diagnostico_mes),

    # Dietas
    path('dietas', view=dieta.index),
    path('dietas/estadisticas', view=dieta.estadisticas),
    path('dietas/estadisticas/evolucion-mensual', view=dieta.estadisticas_dieta_mes),

    # Apoderados
    path('apoderados', view=apoderado.index),
    path('apoderados/<int:id>', view=apoderado.get_apoderado_by_id),
    path('apoderados/dni/<int:dni>', view=apoderado.get_apoderado_by_dni),
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
