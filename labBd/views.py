from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    """View principal do projeto"""

    context = {
        'teste' : 10
    }
    return render(request, 'base.html', context=context)


