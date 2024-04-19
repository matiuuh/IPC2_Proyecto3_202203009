# Tienda/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Tienda1, name='Tiendas'),
    path('Tavlas/', views.Tavlas, name='Tavlas'),
    path('enviar-formulario', views.enviar_formulario, name='enviar_formulario'),
]
