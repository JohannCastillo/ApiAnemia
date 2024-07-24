from rest_framework import serializers
from models.models import Persona

class PersonaSerializer(serializers.Serializer):
    Sexo = serializers.CharField(max_length=1)
    EdadMeses = serializers.IntegerField()
    Peso = serializers.FloatField()
    Talla = serializers.FloatField()
    Hemoglobina = serializers.FloatField()
    Cred = serializers.BooleanField()
    Suplementacion = serializers.BooleanField()
    ProvinciaREN = serializers.CharField(max_length=100)
    DistritoREN = serializers.CharField(max_length=100)

    class Meta:
        fields = '__all__'

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['ProvinciaREN'] = data['ProvinciaREN'].upper()
        data['DistritoREN'] = data['DistritoREN'].upper()
        return data