# Recursos Django
from django.urls import path, re_path
from django.conf.urls import include

# Vistas
from register.views import UserAPI

urlpatterns = [
    re_path(r'^register$', UserAPI.as_view()),    
]