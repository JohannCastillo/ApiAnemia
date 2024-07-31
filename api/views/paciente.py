from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Paciente, Distrito, Apoderado, Apoderado_Paciente
from api.serializers.Paciente import PacienteSerializer, CreatePacienteSerializer


@api_view(['GET'])
def index(request):
    pacientes = Paciente.objects.all()
    return Response({
        "pacientes": PacienteSerializer(pacientes, many=True).data
    }, status=200)


@api_view(['GET'])
def get_pacientes_by_apodeado(request, apoderado_id):
    pacientes = Paciente.objects.filter(
        apoderado_paciente__apoderado_id=apoderado_id)
    return Response({
        "pacientes": PacienteSerializer(pacientes, many=True).data
    }, status=200)


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
        )
        newPaciente.save()
        # Crear relación de paciente con apoderado
        paciente_apoderado = Apoderado_Paciente(
            paciente = newPaciente,
            apoderado = apoderado
        )
        paciente_apoderado.save()
        return Response({
            "paciente": PacienteSerializer(newPaciente).data
        }, status=201)
    except Exception as e:
        print(f"Error al guardar paciente: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)
