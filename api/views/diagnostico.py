from rest_framework.decorators import api_view
from api.models import Diagnostico
from api.serializers.Diagnostico import DiagnosticoSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Q
from api.pagination.pageable import CustomPagination, paginate_results
import random

@api_view(['GET'])
def index(request):
    # Lista de todos los diagnósticos
    diagnosticos = Diagnostico.objects.all()
    data = DiagnosticoSerializer(diagnosticos, many=True).data
    return Response(
        paginate_results(CustomPagination(), request, data)
    , status=200)


"""
Detalle diagnósticos por nivel de gravedad
"""
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
@api_view(['GET'])
def estadisticas_diagnostico_mes(request):
    año = request.GET.get('ano', None)
    mes = request.GET.get('mes', None)

    diagnosticos = Diagnostico.objects.all()
    if año is not None:
        diagnosticos = diagnosticos.filter(created_at__year=año)
    if mes is not None:
        diagnosticos = diagnosticos.filter(created_at__month=mes)


    grouped_diagnosticos = diagnosticos.values('created_at').annotate(
        moderada=Count('dx_anemia', 
        filter=Q(dx_anemia="Anemia Moderada")), 
        severa=Count('dx_anemia', 
        filter=Q(dx_anemia="Anemia Severa")), 
        leve=Count('dx_anemia', filter=Q(dx_anemia="Anemia Leve")), 
        normal=Count('dx_anemia', filter=Q(dx_anemia="Normal")))
   
    grouped_diagnosticos = list(grouped_diagnosticos)
    grouped_diagnosticos.sort(key=lambda x: x['created_at'])

    response = []
    for diagnostico in grouped_diagnosticos:
        date = diagnostico['created_at'].strftime("%Y-%m")
        if not any(x['date'] == date for x in response):
            data_dict = {
                "date" : date,
                "moderada" : diagnostico['moderada'],
                "severa" : diagnostico['severa'],
                "leve" : diagnostico['leve'],
                "normal" : diagnostico['normal'],
                "pronostico" :random.randint(50, 100) # random for testing
            }
            response.append(data_dict)
        else:
            for i in range(len(response)):
                if response[i]['date'] == date:
                    response[i]['moderada'] += diagnostico['moderada']
                    response[i]['severa'] += diagnostico['severa']
                    response[i]['leve'] += diagnostico['leve']
                    response[i]['normal'] += diagnostico['normal']
                    break
    return Response(response, status=200)