from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Paciente, Distrito, Apoderado, Apoderado_Paciente
from api.pagination.pageable import CustomPagination, paginate_results
from api.serializers.Paciente import PacienteSerializer, CreatePacienteSerializer


@api_view(['GET'])
def index(request):
    pacientes = Paciente.objects.all()
    return Response( PacienteSerializer(pacientes, many=True).data, status=200)


@api_view(['GET'])
def get_pacientes_by_apoderado(request, apoderado_id):
    pacientes = Paciente.objects.filter(
        apoderado_paciente__apoderado_id=apoderado_id)
    return Response(
        PacienteSerializer(pacientes, many=True).data
        , status=200
    )

@api_view(['GET'])
def get_pacientes_by_apoderado_user(request):
    user = request.userdb
    apoderado = Apoderado.objects.filter(email=user.email).first()
    pacientes = Paciente.objects.filter(
        apoderado_paciente__apoderado_id=apoderado.id)
    
    return Response(
        paginate_results(CustomPagination(), request, pacientes, PacienteSerializer)
    , status=200)
    # return Response(
    #     PacienteSerializer(pacientes, many=True).data
    #     , status=200
    # )

@api_view(['GET'])
def get_paciente_by_id(request, id):
    try:
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return Response({"error": "El paciente no existe"}, status=404)
    return Response(PacienteSerializer(paciente).data, status=200)

@api_view(['GET'])
def get_paciente_by_dni(request, dni):
    try:
        paciente = Paciente.objects.get(dni=dni)
    except Paciente.DoesNotExist:
        return Response({"error": "El paciente no existe"}, status=404)
    return Response(PacienteSerializer(paciente).data, status=200)

@api_view(['GET'])
def get_paciente_by_cnv(request, cnv):
    try: 
        paciente = Paciente.objects.get(codigo_cnv=cnv)
    except Paciente.DoesNotExist:
        return Response({"error": "El paciente no existe"}, status=404)
    return Response(PacienteSerializer(paciente).data, status=200)


@api_view(['POST'])
def create(request, apoderado_id):
    paciente = CreatePacienteSerializer(data=request.data)
    paciente.is_valid(raise_exception=True)
    try:
        apoderado = Apoderado.objects.get(id=apoderado_id)
        newPaciente = Paciente(
            nombre = paciente.data['nombre'],
            sexo = paciente.data['sexo'],
            fecha_nacimiento = paciente.data['fecha_nacimiento'],
            distrito = Distrito.objects.get(id=paciente.data['distrito']),
            codigo_cnv = paciente.data['codigo_cnv'],
            dni = paciente.data.get('dni', None),
        )
        newPaciente.save()
        # Crear relación de paciente con apoderado
        paciente_apoderado = Apoderado_Paciente(
            paciente = newPaciente,
            apoderado = apoderado
        )
        paciente_apoderado.save()
        return Response(PacienteSerializer(newPaciente).data, status=201)
    except Exception as e:
        print(f"Error al guardar paciente: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)

@api_view(['POST'])
def create_by_user(request):
    paciente = CreatePacienteSerializer(data=request.data)
    paciente.is_valid(raise_exception=True)
    user = request.userdb
    
    try:
        apoderado = Apoderado.objects.filter(email=user.email).first()
        newPaciente = Paciente(
            nombre = paciente.data['nombre'],
            sexo = paciente.data['sexo'],
            fecha_nacimiento = paciente.data['fecha_nacimiento'],
            distrito = Distrito.objects.get(id=paciente.data['distrito']),
            codigo_cnv = paciente.data['codigo_cnv'],
            dni = paciente.data.get('dni', None),
        )
        newPaciente.save()
        # Crear relación de paciente con apoderado
        paciente_apoderado = Apoderado_Paciente(
            paciente = newPaciente,
            apoderado = apoderado
        )
        paciente_apoderado.save()
        return Response(PacienteSerializer(newPaciente).data, status=201)
    except Exception as e:
        print(f"Error al guardar paciente: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)