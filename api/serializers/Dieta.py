from rest_framework import serializers
from api.models import Dieta
from api.serializers.Paciente import PacienteSerializer


class DietaSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()

    class Meta :
        model = Dieta
        fields = "__all__"

    def get_paciente(self, obj : Dieta):
        paciente = obj.paciente
        return PacienteSerializer(paciente).data