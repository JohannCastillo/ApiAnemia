from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Diagnostico, Dieta
from chatbot.utils.dieta_gpt import DICTIONARY_DIETA, RESULTADOS_DIETA
from models.utils.diagnostico_utils import calcular_edad_en_meses
from .services.dalle_generator import DalleGenerator


@api_view(["POST"])
def generate_image(request):
    prompt = request.data.get("prompt")
    size = request.data.get("size", "1024x1024")
    quality = request.data.get("quality", "standard")
    n = request.data.get("n", 1)

    if not prompt:
        return Response({"error": "Se requiere un prompt"}, status=400)

    generator = DalleGenerator()
    try:
        image_url = generator.generate_image(prompt, size, quality, n)
        return Response({"image_url": image_url})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

def generate_image_util(prompt):
    size = "1024x1024"
    quality = "standard"
    n = 1

    if not prompt:
        return Response({"error": "Se requiere un prompt"}, status=400)

    generator = DalleGenerator()
    try:
        image_url = generator.generate_image(prompt, size, quality, n)
        return Response({"image_url": image_url})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def gen_dieta(request, dieta_id):
    dieta = Dieta.objects.select_related("paciente").get(id=dieta_id)
    string_dieta = ""

    for key, value in dieta.__dict__.items():
        if key.startswith("frec"):
            string_dieta += f"{DICTIONARY_DIETA[key]}: {value}\n"

    prompt = f""" Un infante peruano de entre 3 y 35 meses
Edad: {calcular_edad_en_meses(dieta.paciente.fecha_nacimiento)} meses
Sexo: {dieta.paciente.sexo}
Lugar de procedencia: {dieta.paciente.distrito.distrito}

Resultado: {RESULTADOS_DIETA[dieta.dx_dieta]}
Dependiendo si el resultado es peor, haz el niño más triste. Si es mejor, hazlo más feliz.
Foto hiperrealista
Con el fondo en su casa o en algún lugar de Perú
Solo el niño, sin ningún texto u otro detalle
"""
    return generate_image_util(prompt)

@api_view(["GET"])
def gen_predict(request, diag_id):
    diagnostico = Diagnostico.objects.select_related("paciente").get(id=diag_id)

    paciente = diagnostico.paciente

    prompt = f""" Un infante peruano de entre 3 y 35 meses
hemoglobina: {diagnostico.hemoglobina}
peso: {diagnostico.peso} cm
talla: {diagnostico.talla} Kg
Control de desarrollo y crecimiento: {'Sí' if diagnostico.cred else 'No'}
Suplementación: {'Sí' if diagnostico.suplementacion else 'No'}
Edad en meses: {calcular_edad_en_meses(paciente.fecha_nacimiento)}
Sexo: {paciente.sexo}

Resultado: {diagnostico.dx_anemia.nivel}
Dependiendo si el resultado es peor, haz el niño más triste. Si es mejor, hazlo más feliz.
Foto hiperrealista
Con el fondo en su casa o en algún lugar de Perú
Solo el niño, sin ningún texto u otro detalle
"""
    return generate_image_util(prompt)