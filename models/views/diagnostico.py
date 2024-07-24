from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
def index(request):
    return Response("Modelo para determinal el nivel de severidad de anemia en niños", status=200)