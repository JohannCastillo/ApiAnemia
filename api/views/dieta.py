from api.serializers.Dieta import DietaSerializer
from rest_framework.decorators import api_view
from api.models import Dieta
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Q
from api.pagination.pageable import CustomPagination, paginate_results
import random

@api_view(['GET'])
def index(request):
    # Lista de todos las dietas
    dietas = Dieta.objects.all()
    data = DietaSerializer(dietas, many=True).data

    return Response(
        paginate_results(CustomPagination(), request, data)
    , status=200)


"""
Detalle dietas por nivel de riesgo
"""
@api_view(['GET'])
def estadisticas(request):
    id_paciente = request.GET.get('idPaciente', None)
    # Lista de todos las dietas
    dietas = Dieta.objects.all()

    if id_paciente is not None:
        dietas = dietas.filter(paciente__id=id_paciente)

    anemia_baja = dietas.filter(dx_dieta=1)
    anemia_alta = dietas.filter(dx_dieta=2)
    anemia_moderada = dietas.filter(dx_dieta=3)
 
    estadisticas = {
        'anemia baja': {
            'total': anemia_baja.count(),
            'dietas' : DietaSerializer(anemia_baja, many=True).data,
        },
        'anemia moderada': {
            'total': anemia_moderada.count(),
            'dietas' : DietaSerializer(anemia_moderada, many=True).data,
        },
        'anemia alta': {
            'total': anemia_alta.count(),
            'dietas' : DietaSerializer(anemia_alta, many=True).data,
        },
        "total": len(dietas)
    }

    return Response(estadisticas, status=200)


""" Devolver dietas agrupadas por mes y año de created_at de la dieta """
@api_view(['GET'])
def estadisticas_dieta_mes(request):
    año = request.GET.get('ano', None)
    mes = request.GET.get('mes', None)

    dietas = Dieta.objects.all()
    if año is not None:
        dietas = dietas.filter(created_at__year=año)
    if mes is not None:
        dietas = dietas.filter(created_at__month=mes)


    grouped_dietas = dietas.values('created_at').annotate(
        alta=Count('dx_dieta', filter=Q(dx_anemia=2)), 
        moderada=Count('dx_dieta', filter=Q(dx_dieta=3)), 
        baja=Count('dx_dieta', filter=Q(dx_anemia=1))), 
   
    grouped_dietas = list(grouped_dietas)
    grouped_dietas.sort(key=lambda x: x['created_at'])

    response = []
    for dieta in grouped_dietas:
        date = dieta['created_at'].strftime("%Y-%m")
        if not any(x['date'] == date for x in response):
            data_dict = {
                "date" : date,
                "moderada" : dieta['moderada'],
                "alta" : dieta['alta'],
                "baja" : dieta['baja'],
                "pronostico" :random.randint(50, 100) # random for testing
            }
            response.append(data_dict)
        else:
            for i in range(len(response)):
                if response[i]['date'] == date:
                    response[i]['moderada'] += dieta['moderada']
                    response[i]['alta'] += dieta['alta']
                    response[i]['baja'] += dieta['baja']
                    break
    return Response(response, status=200)