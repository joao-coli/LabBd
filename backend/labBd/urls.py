from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('user/', views.index, name="user"),
    path('cadastro_usuario/', views.cadastrar_usuario, name="cadastro_usuario"),
    path('cadastro_veiculo/', views.cadastrar_veiculo, name="cadastro_veiculo"),
    path('procurar_carona/', views.procurar_carona, name="procurar_carona"),
    path('cadastro_ponto/', views.cadastrar_ponto, name="cadastro_ponto"),
    path('cadastro_oferta_carona/', views.cadastrar_oferta_carona, name="cadastro_oferta_carona"),
    path('consulta_oferta_caronas/', views.consultar_oferta_caronas, name="consulta_oferta_caronas"),
    path('listar_pontos/', views.listar_pontos, name="listar_pontos"),
    path('', views.index, name="index")

]