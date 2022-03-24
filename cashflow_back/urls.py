from django.urls import path, include, re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from django.conf import settings
from django.conf.urls.static import static

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^cashflow/', include('login.urls')),
    re_path(r'^cashflow/', include('register.urls')),
    re_path(r'^cashflow/', include('categorias.urls')),
    re_path(r'^cashflow/', include('flujos.urls')),
    re_path(r'^cashflow/', include('indicadores.urls')),
    re_path(r'^cashflow/', include('reporte.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]