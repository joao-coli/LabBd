from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    """View principal do projeto"""

    buttons = [
        {'text': 'Cadastrar usuário', 'url': 'cadastro_usuario/'},
        {'text': 'Cadastrar veículo', 'url': 'cadastro_veiculo/'},
        {'text': 'Procurar carona', 'url': ''},
        {'text': 'Oferecer carona', 'url': ''},
        {'text': 'Caronas realizadas', 'url': ''},
        {'text': 'Pontos cadastrados', 'url': ''}
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


