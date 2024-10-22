from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.registro, name='registro'),
    path('salir/', views.cerrar_sesion, name='salir'),
    path('home/', views.home, name='home'),
    path('modificar/<str:username>', views.modificar, name='modificar'),
    path('eliminar/<str:username>', views.eliminar_usuario, name='eliminar'),
    path('perfil/', views.perfil, name='perfil'),

]
