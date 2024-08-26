from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
