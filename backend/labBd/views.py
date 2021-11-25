from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import *

from django.db import connection
from datetime import datetime

from django.contrib.auth.hashers import make_password

@login_required
def index(request):
    """View principal do projeto"""

    if request.user.is_superuser: 
        buttons = [
                {'text': 'Cadastrar usuário', 'url': 'cadastro_usuario/'},
                {'text': 'Cadastrar veículo', 'url': 'cadastro_veiculo/'},
                {'text': 'Procurar carona', 'url': 'procurar_carona/'},
                {'text': 'Oferecer carona', 'url': 'cadastro_oferta_carona/'},
                {'text': 'Caronas realizadas', 'url': ''},
                {'text': 'Pontos cadastrados', 'url': 'listar_pontos/'}

            #{'text': 'Cadastrar Ponto', 'url': 'cadastro_ponto/'}
        ]
    else:
        buttons = [
                {'text': 'Cadastrar usuário', 'url': '#'},
                {'text': 'Cadastrar veículo', 'url': 'cadastro_veiculo/'},
                {'text': 'Procurar carona', 'url': 'procurar_carona/'},
                {'text': 'Oferecer carona', 'url': 'cadastro_oferta_carona/'},
                {'text': 'Caronas realizadas', 'url': ''},
                {'text': 'Pontos cadastrados', 'url': 'listar_pontos/'}

            #{'text': 'Cadastrar Ponto', 'url': 'cadastro_ponto/'}
        ]

    context = {
        'buttons': buttons
    }

    return render(request, 'home.html', context=context)

@login_required
def consultar_oferta_caronas(request):
    cmd = ''' SELECT data_partida as "Data Partida",
    horario_partida as "Horário partida",
    vagas_ofertadas as "Vagas Ofertadas",
    vagas_disponiveis as "Vagas Disponíveis",
    modelo as "Modelo do veículo", 
    placa as "Placa"
    FROM lista_caronas_oferecidas WHERE id_usuario = 1 
    ''' # trocar id usuario
    with connection.cursor() as cursor:
        cursor.execute(cmd)
        caronas_oferecidas = cursor.fetchall()
    return render(request, 'consulta_oferta_caronas.html',{'caronas_oferecidas': caronas_oferecidas})

@login_required
def cadastrar_usuario(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            dict_params = request.POST.copy()
            dict_params.pop('csrfmiddlewaretoken')
            dict_params['password'] = make_password(dict_params['password'])
            if 'cad_cbox_motorista' in request.POST.keys():
                dict_params.pop('cad_cbox_motorista')
                if 'cad_cbox_passageiro' in request.POST.keys():
                    print("Cadastra os dois")
                    dict_params.pop('cad_cbox_passageiro')
                    cmd = ''' call cadastropassageiromotorista ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',{10},'{11}',{12},{13},{14},{15},{16},{17}) '''.format(
                        make_password(request.POST['password']), request.POST['cad_cpf'], request.POST['cad_numero_cnh'], request.POST['cad_validade_cnh'], request.POST['cad_primeiro_nome'], request.POST['cad_sobrenome'], request.POST['cad_login'], 
                        request.POST['cad_dominio'], request.POST['cad_data_nascimento'], request.POST['cad_logradouro'], 
                        request.POST['cad_numero'], request.POST['cad_cep'], request.POST['cad_ddd1'], request.POST['cad_pref1'], 
                        request.POST['cad_telefone1'], request.POST['cad_ddd2'], request.POST['cad_pref2'], request.POST['cad_telefone2'])
                else:
                    dict_params.pop('cad_cpf')
                    cmd = ''' call cadastromotorista ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9},'{10}',{11},{12},{13},{14},{15},{16}) '''.format(
                        make_password(request.POST['password']), request.POST['cad_numero_cnh'], request.POST['cad_validade_cnh'], request.POST['cad_primeiro_nome'], request.POST['cad_sobrenome'], request.POST['cad_login'], 
                        request.POST['cad_dominio'], request.POST['cad_data_nascimento'], request.POST['cad_logradouro'], 
                        request.POST['cad_numero'], request.POST['cad_cep'], request.POST['cad_ddd1'], request.POST['cad_pref1'], 
                        request.POST['cad_telefone1'], request.POST['cad_ddd2'], request.POST['cad_pref2'], request.POST['cad_telefone2'])
            elif 'cad_cbox_passageiro' in request.POST.keys():
                dict_params.pop('cad_cbox_passageiro') 
                dict_params.pop('cad_numero_cnh')
                dict_params.pop('cad_validade_cnh')
                print('Cadastra só passageiro')
                cmd = ''' call cadastropassageiro ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}',{10},{11},{12},{13},{14},{15}) '''.format(
                    make_password(request.POST['password']), request.POST['cad_cpf'], request.POST['cad_primeiro_nome'], request.POST['cad_sobrenome'], request.POST['cad_login'], 
                        request.POST['cad_dominio'], request.POST['cad_data_nascimento'], request.POST['cad_logradouro'], 
                        request.POST['cad_numero'], request.POST['cad_cep'], request.POST['cad_ddd1'], request.POST['cad_pref1'], 
                        request.POST['cad_telefone1'], request.POST['cad_ddd2'], request.POST['cad_pref2'], request.POST['cad_telefone2'])
            else:
                return render(request, 'cadastro_usuario.html')
                
            with connection.cursor() as cursor:
                cursor.execute(cmd)
        return render(request, 'cadastro_usuario.html')

    return render(request, 'home.html')


@login_required
def cadastrar_veiculo(request):
    if request.method == 'POST':
        dict_params = request.POST.copy()
        dict_params.pop('csrfmiddlewaretoken')
        cmd = ''' call CadastroPossui 
        (1, '{0}','{1}',{3},'{2}','{4}') 
        '''.format(*dict_params.values())
        
        with connection.cursor() as cursor:
            cursor.execute(cmd)

    return render(request, 'cadastro_veiculo.html', {'range':range(6)})

@login_required
def procurar_carona(request):
    if request.method == 'POST':
        print(request.POST["cad_local_partida"])
    return render(request, 'procurar_carona.html')

@login_required
def cadastrar_ponto(request):
    if request.method == 'POST':
        dict_params = request.POST.copy()
        dict_params.pop('csrfmiddlewaretoken')
        cmd = ''' call insere_ponto ({2},{3},'{6}',{5},'{4}','{0}','{1}') '''.format(*dict_params.values())

        with connection.cursor() as cursor:
            cursor.execute(cmd)
            
    return render(request, 'cadastro_ponto.html')


@login_required
def cadastrar_oferta_carona(request):
    if request.method == 'POST':
        dict_params = request.POST.copy()
        dict_params.pop('csrfmiddlewaretoken')
        datatempo = datetime.strptime(dict_params["cad_oferta_data_hora"], '%Y-%m-%dT%H:%M')
        dict_params["cad_oferta_data_hora"] = datatempo.strftime('%Y-%m-%d')
        dict_params["cad_oferta_hora"] = datatempo.strftime('%H:%M:%S')
        cmd = ''' call cadastro_oferta_carona ({0},'{4}','{5}',{1},'{3}','{2}') '''.format(*dict_params.values())
        with connection.cursor() as cursor:
            cursor.execute(cmd)

    # Trocar depois o segundo parâmetro pro id do motorista
    cmd_veiculos = '''SELECT lista_veiculos_disponiveis('lista_veiculos',1); # precisa id_usuario
            FETCH ALL FROM lista_veiculos'''
    cmd_pontos = '''SELECT pontos('pontos');
                    FETCH ALL FROM pontos'''
    with connection.cursor() as cursor:
        cursor.execute(cmd_veiculos)
        lista_veiculos = cursor.fetchall()
        cursor.execute(cmd_pontos)
        pontos = cursor.fetchall()
    return render(request, 'cadastro_oferta_carona.html', 
        {'range':range(6), 'lista_veiculos':lista_veiculos, 'pontos': pontos})

@login_required
def listar_pontos(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, ponto_referencia, CEP FROM pontos_registrados ORDER BY nome ")
        pontos = cursor.fetchall()
    return render(request, 'listar_pontos.html', {'pontos':pontos})
    return render(request, 'listar_pontos.html')