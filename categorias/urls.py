# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos Views
from categorias.views import categoryViewAll, categoryViewDetail, categoryEntradaView, categorySalidaView

urlpatterns = [
    re_path(r'^categorias/lista$', categoryViewAll.as_view()),
    re_path(r'^categorias/entradas$', categoryEntradaView.as_view()),
    re_path(r'^categorias/salidas$', categorySalidaView.as_view()),
    re_path(r'^categoria/(?P<pk>\d+)$', categoryViewDetail.as_view()),
]