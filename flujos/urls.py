# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Recursos Views
from flujos.views import flujoViewAll, flujoViewDetail

urlpatterns = [
    re_path(r'^flujos/lista$', flujoViewAll.as_view()),
    re_path(r'^flujo/(?P<pk>\d+)$', flujoViewDetail.as_view()),
]