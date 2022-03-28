# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos Views
from reporte.views import reporteFlujoSalidaView, reporteFlujoEntradaView, reporteIndicadorCPC, reporteIndicadorCPP, reporteIndicadorBNC

urlpatterns = [
    re_path(r'^reporte/flujo/salida/(?P<pk>\d+)$', reporteFlujoSalidaView.as_view()),
    re_path(r'^reporte/flujo/entrada2/(?P<pk>\d+)$', reporteFlujoEntradaView.as_view()),
    re_path(r'^reporte/indicador/cpc/(?P<pk>\d+)$', reporteIndicadorCPC.as_view()),
    re_path(r'^reporte/indicador/cpp/(?P<pk>\d+)$', reporteIndicadorCPP.as_view()),
    re_path(r'^reporte/indicador/bnc/(?P<pk>\d+)$', reporteIndicadorBNC.as_view()),
]