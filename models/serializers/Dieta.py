from rest_framework import serializers
from api.models import Dieta

class DietaSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField(required=True)
    frec_verduras = serializers.IntegerField(required=True)
    frec_carnes_rojas = serializers.IntegerField(required=True)
    frec_aves = serializers.IntegerField(required=True)
    frec_huevos = serializers.IntegerField(required=True)
    frec_pescado = serializers.IntegerField(required=True)
    frec_leche = serializers.IntegerField(required=True)
    frec_menestra = serializers.IntegerField(required=True)
    frec_bocados_dulces = serializers.IntegerField(required=True)
    frec_bebidas_azucaradas = serializers.IntegerField(required=True)
    frec_embutidos = serializers.IntegerField(required=True)
    frec_fritura = serializers.IntegerField(required=True)
    frec_azucar = serializers.IntegerField(required=True)
    frec_desayuno = serializers.IntegerField(required=True)
    frec_almuerzo = serializers.IntegerField(required=True)
    frec_cena = serializers.IntegerField(required=True)
    frec_fruta = serializers.IntegerField(required=True)