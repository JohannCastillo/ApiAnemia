from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.diagnostico_utils import predict
from models.serializers.Persona import PersonaSerializer

modelo = settings.MODEL_DIAGNOSTICO

# Create your views here.


@api_view(['POST'])
def index(request):
    persona = PersonaSerializer(data=request.data)
    persona.is_valid(raise_exception=True)

    print(persona.data)

    try: 
        resultado = predict(modelo, persona.data)
        #TODO guardar diagnóstico en la base de datos
        
        return Response({
            "diagnostico" : resultado
        }, status=200)
    except ValueError as e:
        return Response({"error": "Un valor de los campos de entrada es incorrecto"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)