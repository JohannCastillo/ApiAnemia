from rest_framework import serializers
from api.models import Distrito, Paciente
from rest_framework.validators import UniqueValidator

class PacienteSerializer(serializers.ModelSerializer):
    class Meta :
        model = Paciente
        fields = "__all__"


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = "__all__"
class PacienteSerializerMeta(serializers.ModelSerializer):
    distritoData = serializers.SerializerMethodField()

    def get_distritoData(self, obj):
        return DistritoSerializer(obj.distrito).data
    class Meta :
        model = Paciente
        fields = "__all__"

class PacienteSerializerList(serializers.ModelSerializer):
    distrito = serializers.SerializerMethodField()
    provincia = serializers.SerializerMethodField()
    
    def get_distrito(self, obj):
        return obj.distrito.distrito
    
    def get_provincia(self, obj):
        return obj.distrito.provincia.provincia
    class Meta :
        model = Paciente
        fields = "__all__"

class CreatePacienteSerializer(serializers.ModelSerializer):
    codigo_cnv = serializers.CharField(max_length=20, validators=[
        UniqueValidator(queryset=Paciente.objects.all(), message="El código de certificado de nacido vivo del niño ya se encuentra registrado")]
    )
    dni = serializers.CharField(max_length=8, required=False, validators=[UniqueValidator(queryset=Paciente.objects.all(), message="El dni del niño ya se encuentra registrado")])
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
            'codigo_cnv',
            'dni',
        )