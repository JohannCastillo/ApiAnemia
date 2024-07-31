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
    nombre = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False, unique=True)
    telefono = models.CharField(max_length=9, null=True)
    direccion = models.CharField(max_length=100, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Paciente(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=False)
    fecha_nacimiento = models.DateField(null=False)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=False)
    
class Apoderado_Paciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, null=False)
    

class Diagnostico(models.Model):
    edad_meses = models.IntegerField(null=False)
    peso = models.FloatField(null=False)
    talla = models.FloatField(null=False)
    hemoglobina = models.FloatField(null=False)
    cred = models.BooleanField(default=False)
    suplementacion = models.BooleanField(default=False)
    dx_anemia = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
