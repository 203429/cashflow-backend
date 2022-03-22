# Recursos Django
from django.db import models

# Create your models here.
class categoryModel(models.Model):
    categoria = models.CharField(null=False, max_length=70)
    subcategoria = models.CharField(null=False, max_length=70)