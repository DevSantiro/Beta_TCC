from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import *
from django.http import JsonResponse

# Create your views here.

def index(request):
    
    if request.method == 'POST':
        nome = 'Rodrigo Santiago Claro Filho'
        return nome
        

    

def Index(request):
    return render(request, 'funcoes/index.html') 


def comparar(request):
    
    dados = {}

    if request.method == 'POST':
        if(request.POST.get('act') == 'teste'):

            sequencia1 = request.POST.get('sequencia1') 
            sequencia2 = request.POST.get('sequencia2') 

            tamanho1 = int(request.POST.get('tamanho1'))
            tamanho2 = int(request.POST.get('tamanho2'))
            comparacao = ''
            indice = 0

            #for indice in range(len(sequencia)):
            if (tamanho1 > tamanho2):
                while indice < len(sequencia1):
                    try:
                        if(sequencia1[indice] == sequencia2[indice]):
                            comparacao += '<span class="verde">'+sequencia1[indice]+'</span>'
                        else:
                            comparacao += '<span class="vermelho">'+sequencia1[indice]+'</span>'
                        
                        print(indice)
                        indice += 1
                    except:
                        comparacao += '<span class="vermelho">'+sequencia1[indice]+'</span>'
                        indice += 1
                    
            else:
                while indice < len(sequencia2):
                    try:
                        if(sequencia1[indice] == sequencia2[indice]):
                            comparacao += '<span class="verde">'+sequencia2[indice]+'</span>'
                        else:
                            comparacao += '<span class="vermelho">'+sequencia2[indice]+'</span>'
                        print(indice)
                        indice += 1
                    except:
                        comparacao += '<span class="vermelho">'+sequencia2[indice]+'</span>'
                        indice += 1



            html = "\
            <div>\
                <h4> Resultados </h4>\
                <b>Teste</b>\
            </div>\
            "

            dados = {
                'seq1': request.POST.get('sequencia1'),
                'seq2': request.POST.get('sequencia2'),
                'html': comparacao,
            }


                        
            return JsonResponse(dados)


        if(request.POST.get('act') == 'RNA'):
            CodonTable = {
                'UUU': 'F', 'UUC': 'F',
                'UUA': 'L', 'UUG': 'L', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
                'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
                'AUG': 'M', #Códon de iniciação
                'GUG': 'V',
                'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
                'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
                'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
                'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
                'UAU': 'Y', 'UUC': 'Y',
                'UUA': 'Stop Códon',
                'UAG': 'Stop Códon',
                'CAU': 'H', 'CAC': 'H',
                'CAA': 'Q', 'CAG': 'Q',
                'AAU': 'N', 'AAC': 'N',
                'AAA': 'K', 'AAG': 'K',
                'GAU': 'D', # VERIFICAR
                'GAC': 'D', # VERIFICAR
                'GAA': 'E', # VERIFICAR
                'GAG': 'E', # VERIFICAR
                'UGU': 'C', 'UGC': 'C',
                'UGA': 'W',
                'UGG': 'R', 'CGU': 'R', 'CGC': 'R', 'CGA': 'R',
                'CGG': 'S', 'AGU': 'S',
                'AGC': 'R', 'AGA': 'R',
                'AGG': 'G', 'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
            }



        dados = {
           'nome1': request.POST.get('nome1'),
           'nome2': request.POST.get('nome2'),
           'sequencia1': request.POST.get('sequencia1'),
           'sequencia2': request.POST.get('sequencia2'),
        }

        sequencia1 = request.POST.get('sequencia1')
        sequencia2 = request.POST.get('sequencia2')

        #print(len(sequencia1))
        #print(len(sequencia2))

        #print(sequencia1[1])

        # Aqui eu identifico qual é menor e realizo a iteração em cima dela
        # Pois os valores após o seu tamanho serão automaticamente "Diferentes"
        x = 0
        resultado = []
        if len(sequencia1) > len(sequencia2):
            maior = len(sequencia1.replace("\n",""))
            for idx in range(len(sequencia2)):
                if (sequencia2[idx] == '\n'):
                    continue
                if sequencia1[idx] == sequencia2[x]:
                    resultado.append('M') # Match
                else:
                    resultado.append('D') # Diferente
                x+=1
        else:
            maior = len(sequencia2.replace("\n",""))
            for idx in range(len(sequencia1)):
                if (sequencia1[idx] == '\n'):
                    continue
                if sequencia2[idx] == sequencia1[x]:
                    resultado.append('M') # Match
                else:
                    resultado.append('D') # Diferente
                x+=1

        #print(resultado)
        print(maior)

        while x != maior:
            resultado.append('D')
            x +=1
        

        #print(x)
        #print(resultado)


        return render(request, "funcoes/comparar.html", 
        {
            'dados': dados, 
            'resultado': resultado
        })

    return render(request, "funcoes/comparar.html")

# Backup

# def comparar(request):
    
#     dados = {}

#     if request.method == 'POST':
#         dados = {
#            'nome1': request.POST.get('nome1'),
#            'nome2': request.POST.get('nome2'),
#            'sequencia1': request.POST.get('sequencia1'),
#            'sequencia2': request.POST.get('sequencia2'),
#         }

#         sequencia1 = request.POST.get('sequencia1')
#         sequencia2 = request.POST.get('sequencia2')

#         #print(len(sequencia1))
#         #print(len(sequencia2))

#         #print(sequencia1[1])

#         # Aqui eu identifico qual é menor e realizo a iteração em cima dela
#         # Pois os valores após o seu tamanho serão automaticamente "Diferentes"
#         x = 0
#         resultado = []
#         if len(sequencia1) > len(sequencia2):
#             maior = len(sequencia1.replace("\n",""))
#             for idx in range(len(sequencia2)):
#                 if (sequencia2[idx] == '\n'):
#                     continue
#                 if sequencia1[idx] == sequencia2[x]:
#                     resultado.append('M') # Match
#                 else:
#                     resultado.append('D') # Diferente
#                 x+=1
#         else:
#             maior = len(sequencia2.replace("\n",""))
#             for idx in range(len(sequencia1)):
#                 if (sequencia1[idx] == '\n'):
#                     continue
#                 if sequencia2[idx] == sequencia1[x]:
#                     resultado.append('M') # Match
#                 else:
#                     resultado.append('D') # Diferente
#                 x+=1

#         #print(resultado)
#         print(maior)

#         while x != maior:
#             resultado.append('D')
#             x +=1
        

#         #print(x)
#         #print(resultado)


#         return render(request, "funcoes/comparar.html", 
#         {
#             'dados': dados, 
#             'resultado': resultado
#         })

#     return render(request, "funcoes/comparar.html")





def formulario(request):
    data = {}
    if request.method == 'POST':
        data['nome'] = request.POST.get('nome', 'nome não encontrado')
        data['active'] = request.POST.get('active', 'active não encontrada')
        data['week'] = request.POST.get('week', 'week não encontrado')
        data['month'] = request.POST.get('month', 'month não encontrado')
    
    return render(request, "funcoes/formulario.html", data)


def geraFita(sequencia):

    fita = ''

    for indice in range(len(sequencia)):

        if sequencia[indice] == 'A':
            fita += 'T'
            continue

        if sequencia[indice] == 'T':
            fita += 'A'      
            continue

        if sequencia[indice] == 'G':
            fita += 'C'
            continue
        
        if sequencia[indice] == 'C':
            fita += 'G'
            continue
        
    return fita


# Teste
def geraFitaCompleta(sequencia):

    fita = ''

    for indice in range(len(sequencia)):

        if sequencia[indice] == 'A':
            fita += sequencia[indice] + 'T'
            continue

        if sequencia[indice] == 'T':
            fita += sequencia[indice] + 'A'      
            continue

        if sequencia[indice] == 'G':
            fita += sequencia[indice] + 'C'
            continue
        
        if sequencia[indice] == 'C':
            fita += sequencia[indice] + 'G'
            continue
        
    return fita



def geraRNAm(sequencia):
    # Acredito que aqui eu vou precisar gerar a FITA para esse RNAm e depois fazer o mesmo.
    RNAm = ''

    for indice in range(len(sequencia)):
        
        if sequencia[indice] == 'A':
            RNAm += 'U'
            continue
        if sequencia[indice] == 'T':
            RNAm += 'A'
            continue
        
        if sequencia[indice] == 'G':
            RNAm += 'C'
            continue

        if sequencia[indice] == 'C':
            RNAm += 'G'
            continue


    return RNAm

def geraAminoacidos(sequencia):
    CodonTable = {
        'UUU': 'Fenilalanina', 'UUC': 'Fenilalanina',
        'UUA': 'Leucina', 'UUG': 'Leucina', 'CUU': 'Leucina', 'CUC': 'Leucina', 'CUA': 'Leucina', 'CUG': 'Leucina',
        'AUU': 'Isoleucina', 'AUC': 'Isoleucina', 'AUA': 'Isoleucina',
        'AUG': 'Metionina', #Códon de iniciação
        'GUG': 'Valina',
        'UCU': 'Serina', 'UCC': 'Serina', 'UCA': 'Serina', 'UCG': 'Serina',
        'CCU': 'Prolina', 'CCC': 'Prolina', 'CCA': 'Prolina', 'CCG': 'Prolina',
        'ACU': 'Treonina', 'ACC': 'Treonina', 'ACA': 'Treonina', 'ACG': 'Treonina',
        'GCU': 'Alanina', 'GCC': 'Alanina', 'GCA': 'Alanina', 'GCG': 'Alanina',
        'UAU': 'Tirosina', 'UUC': 'Tirosina',
        'UUA': 'Stop Códon',
        'UAG': 'Stop Códon',
        'CAU': 'Histidina', 'CAC': 'Histidina',
        'CAA': 'Glutamina', 'CAG': 'Glutamina',
        'AAU': 'Asparagina', 'AAC': 'Asparagina',
        'AAA': 'Lisina', 'AAG': 'Lisina',
        'GAU': 'Aspartato', # VERIFICAR
        'GAC': 'Aspartato', # VERIFICAR
        'GAA': 'Glutamato', # VERIFICAR
        'GAG': 'Glutamato', # VERIFICAR
        'UGU': 'Cisteína', 'UGC': 'Cisteína',
        'UGA': 'Triptofano',
        'UGG': 'Arginina', 'CGU': 'Arginina', 'CGC': 'Arginina', 'CGA': 'Arginina',
        'CGG': 'Serina', 'AGU': 'Serina',
        'AGC': 'Arginina', 'AGA': 'Arginina',
        'AGG': 'Glicina', 'GGU': 'Glicina', 'GGC': 'Glicina', 'GGA': 'Glicina', 'GGG': 'Glicina'
    }

    aminoacidos = {
        'Alanina': 0,
        'Arginina': 0,
        'Asparagina': 0,
        'Ácido aspártico': 0,
        'Ácido glutâmico': 0,
        'Cisteína': 0,
        'Fenilalanina': 0,
        'Glicina': 0,
        'Glutamina': 0,
        'Histidina': 0,
        'Isoleucina': 0,
        'Leucina': 0,
        'Lisina': 0,
        'Metionina': 0,
        'Prolina': 0,
        'Serina': 0,
        'Tirosina': 0,
        'Treonina': 0,
        'Triptofano': 0,
        'Valina': 0,
    }
    indice = 0
    seq_aminoacidos = ''
    while indice < len(sequencia):
        try:
            seqAtual = sequencia[indice] + sequencia[indice+1] + sequencia[indice+2]

            if seqAtual in CodonTable:
                seq_aminoacidos += CodonTable[seqAtual] + ' - '
            
            print(seq_aminoacidos)
            indice += 3
        except:
            break
    
    return seq_aminoacidos

def conversorDNA(request):
    dados = {}
    if request.method == 'POST':

        sequencia = request.POST.get('sequencia')

        # Adenosina se liga uma Timina e toda Guanina, a uma Citosina.

        fita = geraFita(sequencia)

        fitaCompleta = geraFitaCompleta(sequencia)

        RNAm = geraRNAm(sequencia)

        RNAt = ''

        aminoacidos = geraAminoacidos(RNAm)

        data = {
           'sequencia': sequencia,
           'dados': dados,
           'fita': fita,
           'fitaCompleta': fitaCompleta,
           'RNAm': RNAm,
           'aminoacidos': aminoacidos
        }

        return JsonResponse(data)
        

    return render(request, "funcoes/conversorDNA.html")
    