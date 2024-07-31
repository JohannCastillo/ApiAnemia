from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.dieta_utils import predict

modelo = settings.MODEL_DIETA

# Create your views here.


@api_view(['POST'])
def index(request):
    entradas = [
        request.data["FrecVerduras"],
        request.data["FrecCarnR"],
        request.data["FrecAves"],
        request.data["FrecHuev"],
        request.data["FrecPesc"],
        request.data["FrecLeche"],
        request.data["FrecMenestr"],
        1,
        request.data["FrecBebAzuc"],
        request.data["FrecEmbConsv"],
        request.data["FrecFritura"],
        request.data["FrecAzucar"],
        request.data["FrecDesayuno"],
        request.data["FrecAlmuerzo"],
        request.data["FrecCena"],
        request.data["FrecFruta"]
    ]

    print(entradas)

    # print(persona.data)
    try: 
        resultado = predict(modelo, entradas)
        #TODO guardar diagnóstico en la base de datos
        
        return Response({
            "dieta" : resultado
        }, status=200)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)