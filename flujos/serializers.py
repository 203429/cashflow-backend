from rest_framework import serializers

from flujos.models import flujoModel

class flujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = flujoModel
        fields = ('__all__')