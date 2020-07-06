from django.shortcuts import render
from django.http import HttpResponse
from .models import Proteina
# Create your views here.

def index(request):

    return render(request, 'modelagem/index.html')


def listaProteina(request):

    proteinas = Proteina.objects.all()

    return render(request, 'modelagem/lista.html', 
    {
        'proteinas': proteinas
    })

def infoProteina(request, id):
    proteina = Proteina.objects.get(pk=id)

    return render(request, 'modelagem/infoProteina.html', 
    {
        'prot': proteina
    })