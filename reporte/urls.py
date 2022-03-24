# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos Views
from reporte.views import reporteFlujoSalidaView, reporteFlujoEntradaView, reporteIndicadorCPC, reporteIndicadorCPP, reporteIndicadorBNC

urlpatterns = [
    re_path(r'^reporte/flujo/salida$', reporteFlujoSalidaView.as_view()),
    re_path(r'^reporte/flujo/entrada$', reporteFlujoEntradaView.as_view()),
    re_path(r'^reporte/indicador/cpc$', reporteIndicadorCPC.as_view()),
    re_path(r'^reporte/indicador/cpp$', reporteIndicadorCPP.as_view()),
    re_path(r'^reporte/indicador/bnc$', reporteIndicadorBNC.as_view()),
]