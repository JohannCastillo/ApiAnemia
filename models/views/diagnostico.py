from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.diagnostico_utils import predict
from models.serializers.Diagnostico import DiagnosticoSerializer
from api.models import Diagnostico, Persona, Distrito
import datetime


modelo = settings.MODEL_DIAGNOSTICO

# Create your views here.


@api_view(['POST'])
def index(request):
    evaluacion = DiagnosticoSerializer(data=request.data)
    evaluacion.is_valid(raise_exception=True)

    print(evaluacion.data)
    try: 
        # Retirar de evaluacion.data que no se utilizand como entrada para el modelo
        input = evaluacion.data
        input.pop('Nombre') 
        input['Cred'] = 1 if input['Cred'] else 0
        input['Suplementacion'] = 1 if input['Suplementacion'] else 0
        print(input)
        resultado = predict(modelo, input)
        #TODO guardar diagnóstico en la base de datos
        diagnostico = save_diagnostico(evaluacion, resultado)
        print(f"Diagnostico guardado: {diagnostico}")
    
        if diagnostico:
            return Response({
            "diagnostico" : resultado
            }, status=200)
        else:
            return Response({"error": "No se pudo guardar el diagnóstico"}, status=500)
    except ValueError as e:
        print(f"Value Error: {e}")
        return Response({"error": "Un valor de los campos de entrada es incorrecto"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    


def save_diagnostico(evaluacion, diagnostico):
    try:
        persona = Persona.objects.filter(nombre=evaluacion.data['Nombre']).first()
        distrito = Distrito.objects.filter(distrito__iexact=evaluacion.data['DistritoREN']).first()
        # Si no existe, crear persona
        if not persona:
            persona = Persona(
                nombre = evaluacion.data['Nombre'],
                sexo = evaluacion.data['Sexo'],
                distrito = distrito
            )
            persona.save()
        print(f"Persona guardada: {persona}")
        diagnostico = Diagnostico(
            edad_meses = evaluacion.data['EdadMeses'],
            peso = evaluacion.data['Peso'],
            talla = evaluacion.data['Talla'],
            hemoglobina = evaluacion.data['Hemoglobina'],
            cred = evaluacion.data['Cred'],
            suplementacion = evaluacion.data['Suplementacion'],
            dx_anemia = diagnostico,
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
            persona = persona
        )
        diagnostico.save()
        return diagnostico
    except Exception as e:
        print(f"Error al guardar diagnostico: {e}")
        return None
