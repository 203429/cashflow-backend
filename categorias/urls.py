# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos Views
from categorias.views import categoryViewAll, categoryViewDetail

urlpatterns = [
    re_path(r'^categorias/lista$', categoryViewAll.as_view()),
    re_path(r'^categoria/(?P<pk>\d+)$', categoryViewDetail.as_view()),
]