import datetime
from api.models import Dieta, Paciente
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from models.utils.dieta_utils import predict

modelo = settings.MODEL_DIETA

# Create your views here.


@api_view(['POST'])
def index(request):
    paciente = request.data["Paciente"]
    paciente =  Paciente.objects.filter(id=int(paciente)).first()

    entradas = {
        
        "FrecVerduras": request.data["FrecVerduras"],
        "FrecCarnR" : request.data["FrecCarnR"],
        "FrecAves" : request.data["FrecAves"],
        "FrecHuev" : request.data["FrecHuev"],
        "FrecPesc" : request.data["FrecPesc"],
        "FrecLeche" : request.data["FrecLeche"],
        "FrecMenestr": request.data["FrecMenestr"],
        "FrecBocDulcSal" : 3,
        "FrecBebAzuc" : request.data["FrecBebAzuc"],
        "FrecEmbConsv" : request.data["FrecEmbConsv"],
        "FrecFritura" : request.data["FrecFritura"],
        "FrecAzucar" : request.data["FrecAzucar"],
        "FrecDesayuno" : request.data["FrecDesayuno"],
        "FrecAlmuerzo" : request.data["FrecAlmuerzo"],
        "FrecCena" : request.data["FrecCena"],
        "FrecFruta": request.data["FrecFruta"]
    }

    print(entradas.values())

    # print(persona.data)
    try: 
        resultado = predict(modelo, entradas.values())
        
        dieta = save_dieta(entradas, resultado, paciente)
        
        return Response({
            "dieta" : resultado
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