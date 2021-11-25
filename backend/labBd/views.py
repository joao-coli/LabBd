from django.shortcuts import render

from django.http import HttpResponse


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
        print(request.POST["cad_primeiro_nome"])
    return render(request, 'cadastro_usuario.html')

def cadastrar_veiculo(request):
    if request.method == 'POST':
        print(request.POST["cad_primeiro_nome"])
    return render(request, 'cadastro_veiculo.html', {'range':range(6)})

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