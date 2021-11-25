from django.shortcuts import render

from django.http import HttpResponse
from .models import *

from django.db import connection

def index(request):
    """View principal do projeto"""

    buttons = [
        {'text': 'Cadastrar usuário', 'url': 'cadastro_usuario/'},
        {'text': 'Cadastrar veículo', 'url': 'cadastro_veiculo/'},
        {'text': 'Procurar carona', 'url': 'procurar_carona/'},
        {'text': 'Oferecer carona', 'url': 'cadastro_oferta_carona/'},
        {'text': 'Caronas realizadas', 'url': ''},
        {'text': 'Pontos cadastrados', 'url': 'cadastro_ponto/'}
    ]

    context = {
        'buttons': buttons
    }

    return render(request, 'home.html', context=context)


def cadastrar_usuario(request):
    if request.method == 'POST':
        dict_params = request.POST.copy()
        dict_params.pop('csrfmiddlewaretoken')
        if 'cad_cbox_motorista' in request.POST.keys():
            dict_params.pop('cad_cbox_motorista')
            if 'cad_cbox_passageiro' in request.POST.keys():
                print("Cadastra os dois")
                dict_params.pop('cad_cbox_passageiro')
                cmd = ''' call cadastropassageiromotorista ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},'{10}',{11},{12},{13},{14},{15},{16}) '''.format(*dict_params.values())
            else:
                dict_params.pop('cad_cpf')
                print("Cadastra só o motorista")
                cmd = ''' call cadastromotorista ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}',{10},{11},{12},{13},{14},{15}) '''.format(*dict_params.values())
        elif 'cad_cbox_passageiro' in request.POST.keys():
            dict_params.pop('cad_cbox_passageiro') 
            dict_params.pop('cad_numero_cnh')
            dict_params.pop('cad_validade_cnh')
            print('Cadastra só passageiro')
            cmd = ''' call cadastropassageiro ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7},'{8}',{9},{10},{11},{12},{13},{14}) '''.format(*dict_params.values())
        else:
            return render(request, 'cadastro_usuario.html')
            
        with connection.cursor() as cursor:
            cursor.execute(cmd)

    return render(request, 'cadastro_usuario.html')

def cadastrar_veiculo(request):
    if request.method == 'POST':
        print("VITOR")
    cmd = '''SELECT lista_motoristas('motoristas');
                FETCH ALL FROM motoristas'''
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        tabela_motoristas = cursor.fetchall()

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",tabela_motoristas)
        # MOVE ABSOLUTE valor armazenado na tabela FROM lista_veiculos;

        # FETCH 1 FROM lista_veiculos motorista escolhido
    return render(request, 'cadastro_veiculo.html', {'range':range(6), "tabela_motoristas": tabela_motoristas})

def procurar_carona(request):
    if request.method == 'POST':
        print(request.POST["cad_local_partida"])
    return render(request, 'procurar_carona.html')

def cadastrar_ponto(request):
    if request.method == 'POST':
        print(request.POST["cad_ponto_nome"])
    return render(request, 'cadastro_ponto.html')

def cadastrar_oferta_carona(request):
    if request.method == 'POST':
        print(request.POST["cad_oferta_carona_veiculo"])
    return render(request, 'cadastro_oferta_carona.html', {'range':range(6)})