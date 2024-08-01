from rest_framework import serializers
from api.models import Apoderado
from rest_framework.validators import UniqueValidator

class ApoderadoSerializer(serializers.ModelSerializer):
    class Meta :
        model = Apoderado
        fields = "__all__"

class CreateApoderadoSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(max_length=8, 
        validators=[UniqueValidator(queryset=Apoderado.objects.all(), message="El dni de apoderado ya se encuentra registrado")]
    )
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Apoderado.objects.all(), message="El email de apoderado ya se encuentra registrado")])
    telefono = serializers.CharField(max_length=9)
    direccion = serializers.CharField(max_length=100)

    class Meta :
        model = Apoderado
        fields = (
            'dni',
            'nombre',
            'email',
            'telefono',
            'direccion',
        )