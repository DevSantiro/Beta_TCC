from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proteina, DNA
from django.http import JsonResponse
from .forms import DNAForm

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

    # Todas as possiveis contagens zeradas
    dicionario = {'A':0,'R':0,'N':0,'D':0,'E':0,'C':0,'G':0,'Q':0,'H':0,'I':0,'L':0,'K':0,'M':0,'F':0,'P':0,'S':0,'Y':0,'T':0,'W':0,'V':0}
    
    # Aqui será representado a transparência para cada caso
    # Tentei assim não consegui adaptar em uma lista de dicionario mas quem sabe
    # transparencia = ({'A':0, 'tranparencia': 55}, {'R':0},{'N':0},{'D':0},{'E':0},{'C':0},{'G':0},{'Q':0},{'H':0},{'I':0},{'L':0},{'K':0},{'M':0},{'F':0},{'P':0},{'S':0},{'Y':0},{'T':0},{'W':0},{'V':0})
    
    transparencia = {'A':0,'R':0,'N':0,'D':0,'E':0,'C':0,'G':0,'Q':0,'H':0,'I':0,'L':0,'K':0,'M':0,'F':0,'P':0,'S':0,'Y':0,'T':0,'W':0,'V':0}

    
    sequencia = proteina.sequencia
    contador = 0
    
    for i in sequencia:
        if i in dicionario:
            dicionario[i] = dicionario[i] + 1
            contador = contador + 1
    
    # Tentando criar um div dinâmica para retornar através do Render
    # grafico = "<div>"

    for i in dicionario:
        if dicionario[i] > 0:
            transparencia[i] = dicionario[i]  / contador
            #print(transparencia[i])

        else: 
            transparencia[i] = 0

    #print(len(sequencia.replace('\n','')))
    #print(contador)
    
    # grafico += "<div style='width:100px; border:1px solid #111; color:#fff; height:100px; float:left; background-color:rgba(0, 0, 0, "+ str(transparencia) +"')>"+ str(dicionario[i]) + "</div>"
    # grafico += "</div>"

    #print(transparencia)

    # Abri em um arquivo.html somente para visualizar como estão saindo os resultados
    # saida = open("bgl.html","w")
    # saida.write(grafico)
    # saida.close()

    return render(request, 'modelagem/infoProteina.html', 
    {
        'prot': proteina,
        'dados': dicionario,
        'transparencia': transparencia
    })

    #return HttpResponse(grafico)





    # Processo de Modelagem da Proteina a partir de um Pipeline 


# Usar isso nas demais funções, estas condições de IF
def geraFita(sequencia, espacos = False):

    fita = ''
    count = 0

    for indice in range(len(sequencia)):

        if count == 100 and espacos: 
            count = 0
            fita += '<br>'

        if sequencia[indice] == 'A':
            fita += 'T'
            count += 1
            continue

        if sequencia[indice] == 'T':
            fita += 'A'      
            count += 1
            continue

        if sequencia[indice] == 'G':
            fita += 'C'
            count += 1
            continue
        
        if sequencia[indice] == 'C':
            fita += 'G'
            count += 1
            continue
    
    #print(fita)
    return fita


# Teste
def geraFitaCompleta(sequencia):

    fita = ''
    count = 0

    for indice in range(len(sequencia)):

        if count == 70: 
            count = 0
            fita += '<br>'

        if sequencia[indice] == 'A':
            fita += sequencia[indice] + 'T'
            count += 1
            continue

        if sequencia[indice] == 'T':
            fita += sequencia[indice] + 'A'      
            count += 1
            continue

        if sequencia[indice] == 'G':
            fita += sequencia[indice] + 'C'
            count += 1
            continue
        
        if sequencia[indice] == 'C':
            fita += sequencia[indice] + 'G'
            count += 1
            continue
        
    return fita



# def geraRNAm(sequencia):
#     # Acredito que aqui eu vou precisar gerar a FITA para esse RNAm e depois fazer o mesmo.
#     RNAm = ''

#     for indice in range(len(sequencia)):
        
#         if sequencia[indice] == 'A':
#             RNAm += 'U'
#             continue
#         if sequencia[indice] == 'T':
#             RNAm += 'A'
#             continue
        
#         if sequencia[indice] == 'G':
#             RNAm += 'C'
#             continue

#         if sequencia[indice] == 'C':
#             RNAm += 'G'
#             continue


#     return RNAm

def geraRNAm(sequencia):
    # Acredito que aqui eu vou precisar gerar a FITA para esse RNAm e depois fazer o mesmo.
    RNAm = ''

    for indice in range(len(sequencia)):
        
        if sequencia[indice] == 'A':
            RNAm += 'A'
            continue
        if sequencia[indice] == 'T':
            RNAm += 'U'
            continue
        
        if sequencia[indice] == 'G':
            RNAm += 'G'
            continue

        if sequencia[indice] == 'C':
            RNAm += 'C'
            continue


    return RNAm

def geraAminoacidos(sequencia):
    CodonTable = {
        'UUU': 'Fenilalanina', 'UUC': 'Fenilalanina',
        'UUA': 'Leucina', 'UUG': 'Leucina', 'CUU': 'Leucina', 'CUC': 'Leucina', 'CUA': 'Leucina', 'CUG': 'Leucina',
        'AUU': 'Isoleucina', 'AUC': 'Isoleucina', 'AUA': 'Isoleucina',
        'AUG': 'Metionina', #Códon de iniciação
        'GUG': 'Valina', 'GUC': 'Valina', 'GUU': 'Valina',
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
        'UGA': 'Stop Códon',
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
            
            #print(seq_aminoacidos)
            indice += 3
        except:
            break
    
    return seq_aminoacidos


#Problema ... Estou desconsiderando o 1º caractere..... Aqui e na função que quebra linha

def geraSobreposicao(sequencia1, sequencia2):
    sobreposicao = ''

    sequencia1 = sequencia1.rstrip("\n")
    print(sequencia1)
    sequencia2 = sequencia2.rstrip("<br>")

    print(len(sequencia1))
    print(len(sequencia2))
    print(sequencia2)
    
    i = 0

    while i < len(sequencia1):
        sobreposicao += '<span>' + sequencia1[i:i+60] + '<br>' + sequencia2[i:i+60] + '</span><br>'
        i += 60

    return sobreposicao




    # for i in range(len(sequencia)):

    #     try:
    #         if sequencia[i] == '\n':
    #             contadorSeq +=1
    #         else:
    #             novaseq += sequencia[i]
    #             if contadorSeq == 70:
    #                 novaseq += '<br>'
    #                 contadorSeq = -1
                
    #             contadorSeq +=1
    #     except:
    #         continue

    #     try:
    #         if sequencia[i] == '\n':
    #             contadorFita += 1
    #         else:
    #             novafita += sequencia[i]
    #             if contadorFita == 70:
    #                 contadorFita = -1
    #                 novafita += '<br>'
                
    #             contadorFita += 1

    #     except:
    #         continue
        

        # if (contadorFita % 10 == 0 and contadorSeq % 10 == 0):
        #     if contadorFita == 0 or contadorSeq == 0:
        #         pass
        #     else:
        #         sobreposicao = sobreposicao + novaseq + novafita
        #         novaseq = ''
        #         novafita = ''

    # sobreposicao = sobreposicao.rstrip("\n")

    # count = 70

    # while count < len(sequencia):
    #     sobreposicao = sobreposicao[0:count] + '\n' + sobreposicao[count:]
    #     count += 70

    # sobreposicao = sobreposicao + novaseq + novafita

    return sobreposicao



def conversorDNA(request):
    dados = {}
    if request.method == 'POST':

        sequencia = request.POST.get('sequencia')

        # Adenosina se liga uma Timina e toda Guanina, a uma Citosina.

        fita = geraFita(sequencia, True)

        fitaCompleta = geraFitaCompleta(sequencia)

        RNAm = geraRNAm(sequencia)

        RNAm = quebraLinhas(RNAm)

        sobreposicao = geraSobreposicao(sequencia, geraFita(sequencia))

        RNAt = ''

        aminoacidos = geraAminoacidos(RNAm)

        data = {
           'sequencia': sequencia,
           'dados': dados,
           'fita': fita,
           'fitaCompleta': fitaCompleta,
           'RNAm': RNAm,
           'sobreposicao': sobreposicao,
           'aminoacidos': aminoacidos
        }

        return JsonResponse(data)
        

    #return render(request, "funcoes/conversorDNA.html")


def selecionarTipo(request):
    return render(request, "modelagem/selecionar.html")



def listaDNA(request):

    dnas = DNA.objects.all()

    return render(request, 'modelagem/listaDNA.html', 
    {
        'dnas': dnas
    })

def infoDNA(request, id):
    dna = DNA.objects.get(pk=id)

    # Todas as possiveis contagens zeradas
    dicionario = {'A':0,'T':0,'G':0,'C':0}
    
    
    transparencia = {'A':0,'T':0,'G':0,'C':0}

    
    sequencia = dna.sequencia
    contador = 0
    
    for i in sequencia:
        if i in dicionario:
            dicionario[i] = dicionario[i] + 1
            contador = contador + 1
    
    for i in dicionario:
        if dicionario[i] > 0:
            transparencia[i] = dicionario[i]  / contador
            #print(transparencia[i])

        else: 
            transparencia[i] = 0

    #print(len(sequencia.replace('\n','')))
    #print(contador)
    

    return render(request, 'modelagem/infoDNA.html', 
    {
        'dna': dna,
        'dados': dicionario,
        'transparencia': transparencia
    })




def quebraLinhas(sequencia):
    novaseq = ''
    contador = 1
    
    for i in range(len(sequencia)):
        try:
            novaseq += sequencia[contador-1]
            if contador % 60 == 0:
                novaseq += '<br>'
            
            contador +=1
        except:
            break
    
    return novaseq



def view3d(request):
    return render(request, "modelagem/view.html")


def newButton(request): 
 
    if request.method == 'POST':
        
        form = DNAForm(request.POST)
        
        if form.is_valid():
            dna = form.save(commit=False)
            dna.save()
            return redirect('/listaDNA')
 
    else:   
        form = DNAForm()
        return render(request, 'modelagem/addtask.html', {'form': form})


