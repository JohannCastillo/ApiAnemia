from rest_framework import serializers
from api.models import Distrito, Provincia, Departamento
from api.serializers.Paciente import PacienteSerializer


class DistritoSerializer(serializers.ModelSerializer):
    provincia = serializers.SerializerMethodField()

    def get_provincia(self, obj):
        return obj.provincia.provincia

    class Meta:
        model = Distrito
        fields = "__all__"

    
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = "__all__"
    
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = "__all__"