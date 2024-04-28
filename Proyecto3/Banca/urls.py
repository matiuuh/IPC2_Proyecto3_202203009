from django.urls import path
from . import views

urlpatterns=[
    path('', views.ver_banca, name='Banca'),
    path('cargar-configuracion/', views.cargar_configuracion, name='cargar_configuracion'),
    path('cargar-transacciones/', views.cargar_transacciones, name='cargar_transacciones'),
    path('resetear-datos/', views.resetear_datos, name='resetear_datos'),
    path('consultar-estado-cuenta/', views.consultar_estado_de_cuenta, name='consultar_estado_de_cuenta'),
    path('consultar-ingresos/', views.consultar_ingresos, name='consultar_ingresos'),
]