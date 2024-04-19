from django.urls import path
from . import views

urlpatterns=[
    path('', views.Principal, name='Principal'),
    path('Tablas/', views.Tablas, name='Tablas'),
]