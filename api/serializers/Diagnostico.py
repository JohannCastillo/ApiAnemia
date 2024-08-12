from rest_framework import serializers
from api.models import Diagnostico
from api.serializers.Paciente import PacienteSerializer


class DiagnosticoSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()
    dx_anemia = serializers.CharField(source='dx_anemia.nivel', read_only=True)
    class Meta :
        model = Diagnostico
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Incluir parámetro para excluir el campo de paciente
        self.exclude_paciente = kwargs.pop('exclude_paciente', False)
        super().__init__(*args, **kwargs)

    def get_paciente(self, obj : Diagnostico):
        paciente = obj.paciente
        return PacienteSerializer(paciente).data
    
    def to_representation(self, instance):
        # Si se excluye el campo de paciente, no se incluye en la respuesta
        representation = super().to_representation(instance)
        if self.exclude_paciente:
            representation.pop('paciente', None)
        return representation
    

class DiagnosticoWeekSerializer(serializers.ModelSerializer):
    paciente = serializers.SerializerMethodField()
    dx_anemia = serializers.CharField(source='dx_anemia.nivel', read_only=True)
    class Meta :
        model = Diagnostico
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Incluir parámetro para excluir el campo de paciente
        self.exclude_paciente = kwargs.pop('exclude_paciente', False)
        super().__init__(*args, **kwargs)

    def get_paciente(self, obj : Diagnostico):
        paciente = obj.paciente
        return PacienteSerializer(paciente).data
    
    def to_representation(self, instance):
        # Si se excluye el campo de paciente, no se incluye en la respuesta
        representation = super().to_representation(instance)
        if self.exclude_paciente:
            representation.pop('paciente', None)
        return representation