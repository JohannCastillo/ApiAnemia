from api.models import Distrito, Departamento, Provincia
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers.Ubigeos import *

@api_view(['GET'])
def index(request):
    # Lista departamentos, provincias y distritos
    departamentos = Departamento.objects.all().order_by('departamento')
    provincias = Provincia.objects.all().order_by('provincia')
    distritos = Distrito.objects.all().order_by('distrito')
    return Response({
        'departamentos': DepartamentoSerializer(departamentos, many=True).data,
        'provincias': ProvinciaSerializer(provincias, many=True).data,
        'distritos': DistritoSerializer(distritos, many=True).data,
    }, status=200)

@api_view(['GET'])
def provincias(request):
    provincias = Provincia.objects.all().order_by('provincia')
    return Response(ProvinciaSerializer(provincias, many=True).data, status=200)

@api_view(['GET'])
def departamentos(request):
    departamentos = Departamento.objects.all().order_by('departamento')
    return Response(DepartamentoSerializer(departamentos, many=True).data, status=200)

@api_view(['GET'])
def distritos(request):
    distritos = Distrito.objects.all().order_by('distrito')
    return Response(DistritoSerializer(distritos, many=True).data, status=200)

@api_view(['GET'])
def get_distrito_by_provincia_id(request, provincia_id):
    try:
        distritos = Distrito.objects.filter(provincia_id=provincia_id)
        return Response(DistritoSerializer(distritos, many=True).data, status=200)
    except Exception as e:
        print(f"Error al obtener distritos: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)