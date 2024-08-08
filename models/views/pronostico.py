from http.client import HTTPResponse
from ApiAnemia import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models.utils.pronostico_utils import predecir_segun_fechas
# Create your views here.

modelo = settings.MODEL_PRONOSTICO

@api_view(['POST'])
def index(request):
    entradas = [
        request.data["anho_inicio"],
        request.data["anho_fin"],
    ]

    print(modelo)
    print(entradas)

    # print(persona.data)
    try: 
        resultado = predecir_segun_fechas(modelo, entradas[0], entradas[1])
        print("resultado completo")
        # img_buffer = generar_imagen(resultado)
        print("imagen generada")
        
        response = Response({
            # "imagen": img_buffer,
            "linea": resultado["yhat"],
            "fechas": resultado["ds"]
        }, status=200)
        return response
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)