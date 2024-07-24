from django.db import models

# Create your models here.

class Persona(models.Model):
    sexo = models.CharField(max_length=1)
    edad_meses = models.IntegerField()
    peso = models.FloatField()
    talla = models.FloatField()
    hemoglobina = models.FloatField()
    cred = models.BooleanField()
    suplementacion = models.BooleanField()
    provincia_ren = models.CharField(max_length=100)
    distrito_ren = models.CharField(max_length=100)


class Diagnostico(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    dx_anemia = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)