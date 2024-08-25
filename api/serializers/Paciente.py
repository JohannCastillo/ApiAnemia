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

class UpdatePacienteSerializer(serializers.ModelSerializer):
    codigo_cnv = serializers.CharField(max_length=20)
    dni = serializers.CharField(max_length=8, required=False)
    nombre = serializers.CharField(max_length=100)
    sexo = serializers.CharField(max_length=1)
    fecha_nacimiento = serializers.DateField()
    distrito = serializers.IntegerField()

    class Meta:
        model = Paciente
        fields = '__all__'

    def validate_codigo_cnv(self, value):
        # Obtener el ID del objeto que se está editando
        paciente_id = self.instance.id if self.instance else None

        # Verificar si el código ya existe en otro objeto
        if Paciente.objects.filter(codigo_cnv=value).exclude(id=paciente_id).exists():
            raise serializers.ValidationError("El código de certificado de nacido vivo del niño ya se encuentra registrado")

        return value
    
    def validate_dni(self, value):
        # Obtener el ID del objeto que se está editando
        paciente_id = self.instance.id if self.instance else None

        # Verificar si el dni ya existe en otro objeto
        if Paciente.objects.filter(dni=value).exclude(id=paciente_id).exists():
            raise serializers.ValidationError("El dni del niño ya se encuentra registrado")

        return value
