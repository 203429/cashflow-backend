# Recursos Rest Framework
from rest_framework import serializers

# Recursos locales
from indicadores.models import indicadorModel

class indicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = indicadorModel
        fields = ('__all__')