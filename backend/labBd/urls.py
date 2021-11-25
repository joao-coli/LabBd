from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('user/', views.index, name="user"),
    path('cadastro_usuario/', views.cadastrar_usuario, name="cadastro_usuario"),
    path('cadastro_ponto/', views.cadastrar_ponto, name="cadastro_ponto"),
    path('cadastro_oferta_carona/', views.cadastrar_oferta_carona, name="cadastro_oferta_carona"),
    path('', views.index, name="index")

]