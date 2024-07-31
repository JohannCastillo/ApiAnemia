from django.db import models

class Departamento(models.Model):
    departamento = models.CharField(max_length=100)


class Provincia(models.Model):
    provincia = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)


class Distrito(models.Model):
    distrito = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)


class Persona(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=False)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=False)


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
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
