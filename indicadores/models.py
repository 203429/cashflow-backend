# Recursos Django
from django.db import models

class indicadorModel(models.Model):
    fecha = models.CharField(null=False, max_length=80, default='')
    razon = models.CharField(null=False, max_length=80)
    cantidad = models.BigIntegerField(null=False)
    tipo = models.CharField(null=False, max_length=10, default='')