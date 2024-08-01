from rest_framework import serializers
from api.models import Diagnostico

class DiagnosticoSerializer(serializers.ModelSerializer):
    Paciente = serializers.IntegerField()
    Peso = serializers.FloatField()
    Talla = serializers.FloatField()
    Hemoglobina = serializers.FloatField()
    Cred = serializers.BooleanField()
    Suplementacion = serializers.BooleanField()
    fecha_diagnostico = serializers.DateField(required=False)
    
    class Meta :
        model = Diagnostico
        fields = (
            'Paciente',
            'Peso',
            'Talla',
            'Hemoglobina',
            'Cred',
            'Suplementacion',
            'fecha_diagnostico',
        )