from rest_framework import serializers
from api.models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta :
        model = Paciente
        fields = "__all__"

class CreatePacienteSerializer(serializers.ModelSerializer):
    distrito = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    sexo = serializers.CharField(max_length=1)
    fecha_nacimiento = serializers.DateField()

    class Meta :
        model = Paciente
        fields = (
            'nombre',
            'sexo',
            'fecha_nacimiento',
            'distrito',
        )