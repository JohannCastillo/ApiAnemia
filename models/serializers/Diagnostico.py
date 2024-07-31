from rest_framework import serializers
from api.models import Diagnostico

class DiagnosticoSerializer(serializers.ModelSerializer):
    Paciente = serializers.IntegerField()
    Peso = serializers.FloatField()
    Talla = serializers.FloatField()
    Hemoglobina = serializers.FloatField()
    Cred = serializers.BooleanField()
    Suplementacion = serializers.BooleanField()

    
    class Meta :
        model = Diagnostico
        fields = (
            'Paciente',
            'Peso',
            'Talla',
            'Hemoglobina',
            'Cred',
            'Suplementacion',
        )