from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'funcoes/index.html') 


def Index(request):
    return render(request, 'funcoes/index.html') 


def comparar(request):
    
    dados = {}

    if request.method == 'POST':
        dados = {
           'nome1': request.POST.get('nome1'),
           'nome2': request.POST.get('nome2'),
           'sequencia1': request.POST.get('sequencia1'),
           'sequencia2': request.POST.get('sequencia2'),
        }

        sequencia1 = request.POST.get('sequencia1')
        sequencia2 = request.POST.get('sequencia2')

        print(len(sequencia1))
        print(len(sequencia2))

        print(sequencia1[1])

        # Aqui eu identifico qual é menor e realizo a iteração em cima dela
        # Pois os valores após o seu tamanho serão automaticamente "Diferentes"
        x = 0
        resultado = []
        if sequencia1 > sequencia2:
            maior = len(sequencia1)
            for idx in range(len(sequencia2)):
                if sequencia1[idx] == sequencia2[x]:
                    resultado.append('M') # Match
                else:
                    resultado.append('D') # Diferente
                x+=1
        else:
            maior = len(sequencia2)
            for idx in range(len(sequencia1)):
                if sequencia2[idx] == sequencia1[x]:
                    resultado.append('M') # Match
                else:
                    resultado.append('D') # Diferente
                x+=1

        print(resultado)
        print(x)

        while x != maior:
            resultado.append('D')
            x +=1
        
        print(x)
        print(resultado)
    return render(request, "funcoes/comparar.html", dados)

        

    


    # else:

    #     return render(request, 'funcoes/comparar.html') 


def formulario(request):
    data = {}
    if request.method == 'POST':
        data['nome'] = request.POST.get('nome', 'nome não encontrado')
        data['active'] = request.POST.get('active', 'active não encontrada')
        data['week'] = request.POST.get('week', 'week não encontrado')
        data['month'] = request.POST.get('month', 'month não encontrado')
    
    return render(request, "funcoes/formulario.html", data)