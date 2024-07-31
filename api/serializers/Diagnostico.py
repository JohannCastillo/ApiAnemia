from rest_framework import serializers
from api.models import Diagnostico
from api.serializers.Paciente import PacienteSerializer


class DiagnosticoSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()

    class Meta :
        model = Diagnostico
        fields = "__all__"

    def get_paciente(self, obj : Diagnostico):
        paciente = obj.paciente
        return PacienteSerializer(paciente).data