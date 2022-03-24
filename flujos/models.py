# Recursos Django
from django.db import models
from django.utils import timezone

from categorias.models import categoryModel

# Create your models here.
class flujoModel(models.Model):
    fecha = models.CharField(null=False, max_length=80)
    tipo = models.CharField(null=False, max_length=10)
    categoria = models.ForeignKey(categoryModel, on_delete=models.CASCADE, null=False)
    descripcion = models.CharField(null=False, max_length=80)
    cantidad = models.BigIntegerField(null=False)