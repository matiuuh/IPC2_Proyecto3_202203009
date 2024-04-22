from django.urls import path
from . import views

urlpatterns=[
    path('', views.ver_banca, name='Banca'),
    path('Tienda/', views.ver_tienda, name='Tienda'),
]