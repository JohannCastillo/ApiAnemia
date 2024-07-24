from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
def index(request):
    return Response("Modelo para recomendación de dieta para la anemia en niños", status=200)