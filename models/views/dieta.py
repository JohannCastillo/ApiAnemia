import datetime
from api.models import Dieta, Paciente
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.dieta_utils import predict
from models.serializers.Dieta import DietaSerializer
from django.shortcuts import get_object_or_404
modelo = settings.MODEL_DIETA

# Create your views here.


@api_view(['POST'])
def index(request):
    serializer = DietaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    paciente = get_object_or_404(Paciente, id=serializer.data['paciente_id'])
    request_body = serializer.data
    entradas = {
        "FrecVerduras": request_body["frec_verduras"],
        "FrecCarnR" : request_body["frec_carnes_rojas"],
        "FrecAves" : request_body["frec_aves"],
        "FrecHuev" : request_body["frec_huevos"],
        "FrecPesc" : request_body["frec_pescado"],
        "FrecLeche" : request_body["frec_leche"],
        "FrecMenestr": request_body["frec_menestra"],
        "FrecBocDulcSal" : request_body["frec_bocados_dulces"],
        "FrecBebAzuc" : request_body["frec_bebidas_azucaradas"],
        "FrecEmbConsv" : request_body["frec_embutidos"],
        "FrecFritura" : request_body["frec_fritura"],
        "FrecAzucar" : request_body["frec_azucar"],
        "FrecDesayuno" : request_body["frec_desayuno"],
        "FrecAlmuerzo" : request_body["frec_almuerzo"],
        "FrecCena" : request_body["frec_cena"],
        "FrecFruta": request_body["frec_fruta"]
    }

    print(entradas.values())

    # print(persona.data)
    try: 
        resultado = predict(modelo, list(entradas.values()))
        
        dieta = save_dieta(entradas, resultado, paciente)
        
        return Response({
            "dieta" : resultado,
            "id" : dieta.id
        }, status=200)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

def save_dieta(evaluacion, dieta, paciente : Paciente):
    try:
        dieta = Dieta(
            frec_verduras = evaluacion["FrecVerduras"],
            frec_carnes_rojas = evaluacion["FrecCarnR"],
            frec_aves = evaluacion["FrecAves"],
            frec_huevos = evaluacion["FrecHuev"],
            frec_pescado = evaluacion["FrecPesc"],
            frec_leche = evaluacion["FrecLeche"],
            frec_menestra = evaluacion["FrecMenestr"],
            frec_bocados_dulc = evaluacion["FrecBocDulcSal"],
            frec_bebidas_az = evaluacion["FrecBebAzuc"],
            frec_embutidos_consv = evaluacion["FrecEmbConsv"],
            frec_fritura = evaluacion["FrecFritura"],
            frec_azucar = evaluacion["FrecAzucar"],
            frec_desayuno = evaluacion["FrecDesayuno"],
            frec_almuerzo = evaluacion["FrecAlmuerzo"],
            frec_cena = evaluacion["FrecCena"],
            frec_fruta = evaluacion["FrecFruta"],
            dx_dieta = dieta,
            paciente = paciente,
            created_at = datetime.datetime.now()
        )
        dieta.save()

        return dieta
    except Exception as e:
        print(f"Error al guardar dieta: {e}")
        return None