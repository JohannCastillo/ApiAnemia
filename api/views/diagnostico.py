from rest_framework.decorators import api_view
from api.models import Diagnostico, Paciente, Nivel_Anemia
from api.serializers.Diagnostico import DiagnosticoSerializer
from api.serializers.Paciente import PacienteSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Q
from api.pagination.pageable import CustomPagination, paginate_results
from django.shortcuts import get_object_or_404
import random
from ApiAnemia import settings


@api_view(['GET'])
def index(request):
    # Lista de todos los diagnósticos
    diagnosticos = Diagnostico.objects.all().select_related('paciente', 'dx_anemia').order_by('-created_at')
    return Response(
        paginate_results(CustomPagination(), request, diagnosticos, DiagnosticoSerializer)
    , status=200)

@api_view(['GET'])
def niveles_anemia(request):
    niveles = Nivel_Anemia.objects.all()
    niveles_anemia = []
    for nivel in niveles:
        dict = {
            "id": nivel.id,
            "nivel" : nivel.nivel
        }
        niveles_anemia.append(dict)

    return Response(
        niveles_anemia
    , status=200)

"""
Detalle diagnósticos por nivel de gravedad y paciente
"""
@api_view(['GET'])
def estadisticas_por_paciente_id(request, id_paciente):
    paciente = get_object_or_404(Paciente, id=id_paciente)
    # Lista de todos los diagnósticos
    nivel_anemia_id = request.GET.get('nivelAnemia', None)

    diagnosticos = Diagnostico.objects.all()
    diagnosticos = diagnosticos.filter(paciente=paciente)

    if nivel_anemia_id is not None:
        diagnosticos = diagnosticos.filter(dx_anemia=nivel_anemia_id)
    
    anemia_severa = diagnosticos.filter(dx_anemia__nivel="Anemia Severa")
    anemia_moderada = diagnosticos.filter(dx_anemia__nivel="Anemia Moderada")
    anemia_leve = diagnosticos.filter(dx_anemia__nivel="Anemia Leve")
    normal = diagnosticos.filter(dx_anemia__nivel="Normal")
    
    estadisticas = {
        'paciente': PacienteSerializer(paciente).data,
        'anemia_severa': {
            'total': anemia_severa.count(),
            'diagnosticos' : paginate_results(CustomPagination(), request, anemia_severa, DiagnosticoSerializer, exclude_paciente=True)
        },
        'anemia_moderada': {
            'total': anemia_moderada.count(),
            'diagnosticos' : paginate_results(CustomPagination(), request, anemia_moderada, DiagnosticoSerializer, exclude_paciente=True)
        },
        'anemia_leve': {
            'total': anemia_leve.count(),
            'diagnosticos' : paginate_results(CustomPagination(), request, anemia_leve, DiagnosticoSerializer, exclude_paciente=True)
        },
        'normal': {
            'total': normal.count(),
            'diagnosticos' : paginate_results(CustomPagination(), request, normal, DiagnosticoSerializer, exclude_paciente=True)
        },
        "total": len(diagnosticos)
    }

    return Response(estadisticas, status=200)


""" Devolver estadísticas agrupadas por mes y año de created_at del diagnóstico """
from models.utils.pronostico_utils import predecir_segun_fechas
prophet = settings.MODEL_PRONOSTICO

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
        moderada=Count('dx_anemia', filter=Q(dx_anemia__nivel="Anemia Moderada")), 
        severa=Count('dx_anemia', filter=Q(dx_anemia__nivel="Anemia Severa")), 
        leve=Count('dx_anemia', filter=Q(dx_anemia__nivel="Anemia Leve")), 
        normal=Count('dx_anemia', filter=Q(dx_anemia__nivel="Normal"))
    )
   
    grouped_diagnosticos = list(grouped_diagnosticos)
    grouped_diagnosticos.sort(key=lambda x: x['created_at'])

    # pronósticos
    pronosticar = predecir_segun_fechas(
        prophet, 
        grouped_diagnosticos[0]['created_at'].strftime("%Y"), # año inicial
        grouped_diagnosticos[-1]['created_at'].strftime("%Y") # año final
    )
 
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
                "pronostico" : pronosticar[pronosticar['ds'].apply(lambda x: x.strftime("%Y-%m") == date)]["yhat"].values[0]
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