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

    dicionario = {'A':0,'R':0,'N':0,'D':0,'E':0,'C':0,'G':0,'Q':0,'H':0,'I':0,'L':0,'K':0,'M':0,'F':0,'P':0,'S':0,'Y':0,'T':0,'W':0,'V':0}
    sequencia = proteina.sequencia
    #count = sequencia.count()
    for i in sequencia:
        if i in dicionario:
            dicionario[i] = dicionario[i] + 1
    
    # print(dicionario)

    transparencia = 0,5
    grafico = "<div>"

    for i in dicionario:
        if dicionario[i] > 0:
            transparencia = dicionario[i] / len(dicionario)
            grafico += "<div style='width:100px; border:1px solid #111; color:#fff; height:100px; float:left; background-color:rgba(0, 0, 0, "+ str(transparencia) +"')>"+ str(dicionario[i]) + "</div>"
    grafico += "</div>"

    saida = open("bgl.html","w")
    saida.write(grafico)
    saida.close()
    return render(request, 'modelagem/infoProteina.html', 
    {
        'prot': proteina,
        'dados': dicionario,
        'grafico': grafico
    })