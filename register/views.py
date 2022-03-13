# Recursos Django
from django.contrib.auth.models import User

# Recursos Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics

# Recursos Serializer
from .serializers import RegisterSerializer

class UserAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer