from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
def index(request):
    return Response("Modelo para pronóstico de anemia en niños en los próximos años", status=200)