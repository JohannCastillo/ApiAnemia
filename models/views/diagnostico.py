from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.diagnostico_utils import predict, calcular_edad_en_meses
from models.serializers.Diagnostico import DiagnosticoSerializer
from api.models import Diagnostico, Paciente, Nivel_Anemia
import datetime
from models.utils.alerts import alert_diagnostic_to_apoderados

modelo = settings.MODEL_DIAGNOSTICO

# Create your views here.


@api_view(['POST'])
def index(request):
    evaluacion = DiagnosticoSerializer(data=request.data)
    evaluacion.is_valid(raise_exception=True)

    try: 
        paciente = Paciente.objects.filter(id=evaluacion.data['Paciente']).first()
        if not paciente:
            raise ValueError(f"El paciente no se encuentra registrado")
     
        # Retirar de evaluacion.data que no se utilizand como entrada para el modelo
        input = {
            "Sexo":  paciente.sexo,
            "EdadMeses": calcular_edad_en_meses(paciente.fecha_nacimiento),
            "Peso" : evaluacion.data['Peso'],
            "Talla":  evaluacion.data['Talla'],
            "Hemoglobina":  evaluacion.data['Hemoglobina'],
            "Cred" : 1 if evaluacion.data['Cred'] else 0,
            "Suplementacion": 1 if evaluacion.data['Suplementacion'] else 0,
            "ProvinciaREN":  paciente.distrito.provincia.provincia,
            "DistritoREN":  paciente.distrito.distrito   
        }

        resultado = predict(modelo, input)
        
        diagnostico = save_diagnostico(evaluacion, resultado, paciente)
    
        if diagnostico:
            # Dx Anemia != Normal => Enviar email
            if diagnostico.dx_anemia.nivel != "Normal":
                 alert_diagnostic_to_apoderados(paciente, diagnostico)
                
            return Response({
            "diagnostico" : resultado
            }, status=200)
        else:
            return Response({"error": "No se pudo guardar el diagnóstico"}, status=500)
    except ValueError as e:
        print(f"Value Error: {e}")
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": "Ocurrió un error inesperado"}, status=500)
    


"""  Guardar diagnostico en la base de datos """
def save_diagnostico(evaluacion, diagnostico, paciente : Paciente):
    try:
        nivel_anemia = Nivel_Anemia.objects.get(nivel=diagnostico)
        diagnostico = Diagnostico(
            edad_meses = calcular_edad_en_meses(paciente.fecha_nacimiento),
            peso = evaluacion.data['Peso'],
            talla = evaluacion.data['Talla'],
            hemoglobina = evaluacion.data['Hemoglobina'],
            cred = evaluacion.data['Cred'],
            suplementacion = evaluacion.data['Suplementacion'],
            dx_anemia = nivel_anemia,
            paciente = paciente,
            created_at = evaluacion.data.get('fecha_diagnostico', datetime.datetime.now()),
        )
        diagnostico.save()

        return diagnostico
    except Exception as e:
        print(f"Error al guardar diagnostico: {e}")
        return None


