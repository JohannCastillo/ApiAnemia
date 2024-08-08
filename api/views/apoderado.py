from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Apoderado
from api.serializers.Apoderado import ApoderadoSerializer, CreateApoderadoSerializer


@api_view(['GET'])
def index(request):
    apoderados = Apoderado.objects.all()
    return Response(ApoderadoSerializer(apoderados, many=True).data, status=200)

@api_view(['GET'])
def get_apoderado_by_user_id(request, user_id):
    try:
        apoderado = Apoderado.objects.get(usuario=user_id)
    except Apoderado.DoesNotExist:
        return Response({"error": "El usuario de apoderado no existe"}, status=404)
    return Response(ApoderadoSerializer(apoderado).data, status=200)


@api_view(['GET'])
def get_apoderado_by_id(request, id):
    try:
        apoderado = Apoderado.objects.get(id=id)
    except Apoderado.DoesNotExist:
        return Response({"error": "El apoderado no existe"}, status=404)
    return Response(ApoderadoSerializer(apoderado).data, status=200)

@api_view(['GET'])
def get_apoderado_by_dni(request, dni):
    try:
        apoderado = Apoderado.objects.get(dni=dni)
    except Apoderado.DoesNotExist:
        return Response({"error": "El apoderado no existe"}, status=404)
    return Response(ApoderadoSerializer(apoderado).data, status=200)

@api_view(['POST'])
def create(request):
    apoderado = CreateApoderadoSerializer(data=request.data)
    apoderado.is_valid(raise_exception=True)

    try: 
        newApoderado = Apoderado(
            dni = apoderado.data['dni'],
            nombre = apoderado.data['nombre'],
            email = apoderado.data['email'],
            telefono = apoderado.data['telefono'],
            direccion = apoderado.data['direccion']
        )
        newApoderado.save()
        return Response(ApoderadoSerializer(newApoderado).data, status=201)
    except Exception as e:
        print(f"Error al guardar apoderado: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)

@api_view(['PUT'])
def update(request, id):
    try:
        apoderado = Apoderado.objects.get(id=id)
        apoderado.nombre = request.data['nombre']
        apoderado.email = request.data['email']
        apoderado.telefono = request.data['telefono']
        apoderado.direccion = request.data['direccion']
        apoderado.save()
        return Response(ApoderadoSerializer(apoderado).data, status=200)
    except Apoderado.DoesNotExist:
        return Response({"error": "El apoderado no existe"}, status=404)
    except Exception as e:
        print(f"Error al actualizar apoderado: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)
    
@api_view(['GET'])
def get_pacientes_by_apoderado_user(request):
    pass