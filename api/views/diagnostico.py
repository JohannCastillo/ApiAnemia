from rest_framework.decorators import api_view
from api.models import Diagnostico
from api.serializers.Diagnostico import DiagnosticoSerializer
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    # Lista de todos los diagnósticos
    diagnosticos = Diagnostico.objects.all()
    return Response(
        DiagnosticoSerializer(diagnosticos, many=True).data
    , status=200)
