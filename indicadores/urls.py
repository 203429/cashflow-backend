# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos locales
from indicadores.views import indicadorViewAll, indicadorViewDetail

urlpatterns = [
    re_path(r'^indicadores/lista$', indicadorViewAll.as_view()),
    re_path(r'^indicadores/(?P<pk>\d+)$', indicadorViewDetail.as_view()),
]