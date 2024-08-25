from rest_framework.decorators import api_view
from api.models import Diagnostico, Paciente, Nivel_Anemia, Apoderado
from api.serializers.Diagnostico import DiagnosticoSerializer, DiagnosticoWeekSerializer
from api.serializers.Paciente import PacienteSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Q
from api.pagination.pageable import CustomPagination, paginate_results
from django.shortcuts import get_object_or_404
from django.db.models.functions import ExtractYear, ExtractMonth
from ApiAnemia import settings
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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

@api_view(['GET'])
def diagnosticos_user(request):
    # Get Id Paciente from query params
    user = request.userdb

    apoderado = Apoderado.objects.filter(email=user.email).first()

    id_paciente = request.GET.get('id_paciente', None)

    # Calculate the date one week ago
    one_week_ago = datetime.now() - timedelta(weeks=1)

    diagnosticos = Diagnostico.objects.all().select_related('paciente', 'dx_anemia').order_by('-created_at').filter(
        paciente__apoderado_paciente__apoderado_id=apoderado.id,
        created_at__gte=one_week_ago
    )

    if id_paciente is not None:
        diagnosticos = diagnosticos.filter(paciente__id=id_paciente)

    return Response(DiagnosticoWeekSerializer(diagnosticos, many=True).data, status=200)
    


""" Devolver estadísticas agrupadas por mes y año de created_at del diagnóstico """
from models.utils.pronostico_utils import predecir_segun_fechas
from api.utils.pronostico import get_pronostico_value_by_date
prophet = settings.MODEL_PRONOSTICO

@api_view(['GET'])
def estadisticas_diagnostico_mes(request):
    # Params para filtrar por mes y año ej : "2020-01 - 2024-12"
    año_actual = datetime.now().year
    
    rango_from = request.GET.get('rango_from', f"{año_actual-2}-01")
    rango_to = request.GET.get('rango_to', f"{año_actual}-12")
    # formateando rangos
    rango_from = datetime.strptime(rango_from, "%Y-%m")
    rango_to = datetime.strptime(rango_to, "%Y-%m")
    
    diagnosticos = Diagnostico.objects.all()
    
    # set de años y meses disponibles
    years = diagnosticos.annotate(year=ExtractYear('created_at')).values_list('year', flat=True).distinct()
    months = diagnosticos.annotate(month=ExtractMonth('created_at')).values_list('month', flat=True).distinct()
    
    diagnosticos = diagnosticos.filter(created_at__range=[rango_from, rango_to])

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
        rango_from.strftime("%Y"), # año inicial
        rango_to.strftime("%Y") # año final
    )
    print(pronosticar[pronosticar['ds'] < '2019-05'])
 
    response = []
    initial_date = rango_from
    while initial_date <= rango_to:
        response.append({
            'date' : initial_date.strftime("%Y-%m"),
            'moderada' : 0,
            'severa' : 0,
            'leve' : 0,
            'normal' : 0,
            'pronostico' : get_pronostico_value_by_date(pronosticar, initial_date.strftime("%Y-%m"))
        })
        initial_date += relativedelta(months=1)
    
    for diagnostico in grouped_diagnosticos:
        date = diagnostico['created_at'].strftime("%Y-%m")
        for item in response:
            if item['date'] == date:
                item['moderada'] += diagnostico['moderada']
                item['severa'] += diagnostico['severa']
                item['leve'] += diagnostico['leve']
                item['normal'] += diagnostico['normal']
                break
  

    return Response({
        "años" : sorted(list(years)),
        "meses" : sorted(list(months)),
        "reporte": response,
    }, status=200)