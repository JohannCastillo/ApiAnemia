from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    departamento = models.CharField(max_length=100)


class Provincia(models.Model):
    provincia = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)


class Distrito(models.Model):
    distrito = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)


class Apoderado(models.Model):
    dni = models.CharField(max_length=8, null=True, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=True, unique=True)
    telefono = models.CharField(max_length=9, null=True)
    direccion = models.CharField(max_length=100, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Paciente(models.Model):
    codigo_cnv = models.CharField(max_length=20, null=False, unique=True) # Código de certificado de nacido vivo
    dni = models.CharField(max_length=8, null=True, unique=True) 
    nombre = models.CharField(max_length=100, null=False)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=False)
    fecha_nacimiento = models.DateField(null=False)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=False)
    
class Apoderado_Paciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, null=False)
    

class Nivel_Anemia(models.Model):
    nivel = models.CharField(max_length=20)

class Diagnostico(models.Model):
    edad_meses = models.IntegerField(null=False)
    peso = models.FloatField(null=False)
    talla = models.FloatField(null=False)
    hemoglobina = models.FloatField(null=False)
    cred = models.BooleanField(default=False)
    suplementacion = models.BooleanField(default=False)
    # dx_anemia = models.CharField(max_length=20)
    dx_anemia = models.ForeignKey(Nivel_Anemia, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class Dieta(models.Model):
    frec_verduras = models.IntegerField(null=False)
    frec_carnes_rojas = models.IntegerField(null=False)
    frec_aves = models.IntegerField(null=False)
    frec_huevos = models.IntegerField(null=False)
    frec_pescado = models.IntegerField(null=False)
    frec_leche = models.IntegerField(null=False)
    frec_menestra = models.IntegerField(null=False)
    frec_bocados_dulc = models.IntegerField(null=False)
    frec_bebidas_az = models.IntegerField(null=False)
    frec_embutidos_consv = models.IntegerField(null=False)
    frec_fritura = models.IntegerField(null=False)
    frec_azucar = models.IntegerField(null=False)
    frec_desayuno = models.IntegerField(null=False)
    frec_almuerzo = models.IntegerField(null=False)
    frec_cena = models.IntegerField(null=False)
    frec_fruta = models.IntegerField(null=False)
    dx_dieta = models.IntegerField(null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
