from rest_framework import serializers
from api.models import Diagnostico

class DiagnosticoSerializer(serializers.ModelSerializer):
    Nombre = serializers.CharField(max_length=100)
    Sexo = serializers.CharField(max_length=1)
    EdadMeses = serializers.IntegerField()
    Peso = serializers.FloatField()
    Talla = serializers.FloatField()
    Hemoglobina = serializers.FloatField()
    Cred = serializers.BooleanField()
    Suplementacion = serializers.BooleanField()
    ProvinciaREN = serializers.CharField(max_length=100)
    DistritoREN = serializers.CharField(max_length=100)
    
    class Meta :
        model = Diagnostico
        fields = (
            'Nombre',
            'Sexo',
            'EdadMeses',
            'Peso',
            'Talla',
            'Hemoglobina',
            'Cred',
            'Suplementacion',
            'ProvinciaREN',
            'DistritoREN',
        )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['ProvinciaREN'] = data['ProvinciaREN'].upper()
        data['DistritoREN'] = data['DistritoREN'].upper()
        return data