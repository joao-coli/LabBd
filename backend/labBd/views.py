from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    """View principal do projeto"""

    buttons = [
        {'text': 'Cadastrar usuário', 'url': ''},
        {'text': 'Cadastrar veículo', 'url': ''},
        {'text': 'Procurar carona', 'url': ''},
        {'text': 'Oferecer carona', 'url': ''},
        {'text': 'Caronas realizadas', 'url': ''},
        {'text': 'Pontos cadastrados', 'url': ''}
    ]

    context = {
        'buttons': buttons
    }

    return render(request, 'home.html', context=context)


