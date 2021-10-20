from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    """View principal do projeto"""

    context = {
        'teste' : 10
    }
    return render(request, 'home.html', context=context)


