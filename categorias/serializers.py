from rest_framework import serializers

from categorias.models import categoryModel

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categoryModel
        fields = ('__all__')