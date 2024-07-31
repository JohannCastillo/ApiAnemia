from rest_framework import serializers
from api.models import Apoderado

class ApoderadoSerializer(serializers.ModelSerializer):
    class Meta :
        model = Apoderado
        fields = "__all__"

class CreateApoderadoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telefono = serializers.CharField(max_length=9)
    direccion = serializers.CharField(max_length=100)

    class Meta :
        model = Apoderado
        fields = (
            'nombre',
            'email',
            'telefono',
            'direccion',
        )