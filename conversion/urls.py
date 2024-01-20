# En conversion/urls.py
from django.urls import path
from .views import cargar_imagen

urlpatterns = [
    path('cargar-imagen/', cargar_imagen, name='cargar_imagen'),
]
