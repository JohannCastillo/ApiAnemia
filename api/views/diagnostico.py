from rest_framework.decorators import api_view
from api.models import Diagnostico
from api.serializers.Diagnostico import DiagnosticoSerializer
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    # Lista de todos los diagnósticos
    diagnosticos = Diagnostico.objects.all()
    return Response(
        DiagnosticoSerializer(diagnosticos, many=True).data
    , status=200)


@api_view(['GET'])
def estadisticas(request):
    id_paciente = request.GET.get('idPaciente', None)
    # Lista de todos los diagnósticos
    diagnosticos = Diagnostico.objects.all()

    if id_paciente is not None:
        diagnosticos = diagnosticos.filter(paciente__id=id_paciente)

    anemia_severa = diagnosticos.filter(dx_anemia="Anemia Severa")
    anemia_moderada = diagnosticos.filter(dx_anemia="Anemia Moderada")
    anemia_leve = diagnosticos.filter(dx_anemia="Anemia Leve")
    normal = diagnosticos.filter(dx_anemia="Normal")
 
    estadisticas = {
        'anemia severa': {
            'total': anemia_severa.count(),
            'diagnosticos' : DiagnosticoSerializer(anemia_severa, many=True).data,
        },
        'anemia moderada': {
            'total': anemia_moderada.count(),
            'diagnosticos' : DiagnosticoSerializer(anemia_moderada, many=True).data,
        },
        'anemia leve': {
            'total': anemia_leve.count(),
            'diagnosticos' : DiagnosticoSerializer(anemia_leve, many=True).data,
        },
        'normal': {
            'total': normal.count(),
            'diagnosticos' : DiagnosticoSerializer(normal, many=True).data,
        },
        "total": len(diagnosticos)
    }

    return Response(estadisticas, status=200)


""" Devolver estadísticas agrupadas por mes y año de created_at del diagnóstico """
