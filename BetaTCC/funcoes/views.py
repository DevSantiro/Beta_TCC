from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import *
from django.http import JsonResponse
from Bio.Blast.Applications import NcbiblastpCommandline
from io import StringIO ## for Python 3
from Bio.Blast import NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO


# Create your views here.

def index(request):
    
    if request.method == 'POST':
        nome = 'Rodrigo Santiago Claro Filho'
        return nome
        

    

def Index(request):
    return render(request, 'funcoes/index.html') 


def blastp(request):
    dados = {}
    if request.method == 'POST':
        if(request.POST.get('act') == 'blastp'):
            
            sequencia1 = request.POST.get('sequencia1') 
            sequencia2 = request.POST.get('sequencia2') 
            print(sequencia1)
            # Create two sequence files
            seq1 = SeqRecord(Seq(sequencia1),
            id="seq1")
            seq2 = SeqRecord(Seq(sequencia2),
            id="seq2")
            SeqIO.write(seq1, "media\\seq1.fasta", "fasta")
            SeqIO.write(seq2, "media\\seq2.fasta", "fasta")

            # Run BLAST and parse the output as XML
            output = NcbiblastpCommandline(query="media\\seq1.fasta", subject="media\\seq2.fasta", outfmt=5)()[0]
            blast_result_record = NCBIXML.read(StringIO(output))
            # Print some information on the result
            for alignment in blast_result_record.alignments:
                for hsp in alignment.hsps:
                    #print('****Alignment****')
                    #print('sequence:', alignment.title)
                    titulo_alinhamento = alignment.title
                    #print('length:', alignment.length)
                    tamanho = alignment.length
                    #print('e value:', hsp.expect)
                    valorE = hsp.expect
                    #print('###### Query #####')
                    #print(hsp.query)
                    query = hsp.query
                    #print('###### Match #####')
                    #print(hsp.match)
                    match = hsp.match
                    #print('###### Subject ######')
                    #print(hsp.sbjct)
                    subject = hsp.sbjct
                    #print('###########')
        
        i = 0 
        blast = ''
        
        while i < alignment.length:
            blast += '<span style="color:white;">' + query[i:i+60] + '</span><br>' + '<span style="color: yellowgreen;";>' + match[i:i+60] + '</span><br>' + '<span style="color:white">' + subject[i:i+60] + '</span><br><br>'
            i += 60            

        dados = {
           'titulo': titulo_alinhamento,
           'tamanho': tamanho,
           'valorE': valorE,
           'query': query,
           'match': match,
           'subject': subject,
           'blast': blast
        }

    return JsonResponse(dados)
        

# #Forma Correta
def compararTeste(request):
    # pass
    dados = {}

    if request.method == 'POST':
        if(request.POST.get('act') == 'compararTeste'):
            
            ondeestou = 0
            sequencia1 = request.POST.get('sequencia1') 
            sequencia2 = request.POST.get('sequencia2') 

            tamanho1 = int(request.POST.get('tamanho1'))
            tamanho2 = int(request.POST.get('tamanho2'))  
            
            if tamanho1 > tamanho2:
                teste3 = '<div>'
                linha1 = ''
                linha2 = ''
                linha3 = ''

                contador = 0

                while contador < len(sequencia1):
                    # print(contador)
                    linha1 += sequencia1[contador] 
                    
                    try:
                        if sequencia1[contador] == sequencia2[contador]:
                            linha2 += sequencia1[contador]
                        else: 
                            linha2 += '+'
                    except:
                        linha2 += ' '

                    try:
                        linha3 += sequencia2[contador]
                    except:
                        linha3 += ' '
                    
                    contador += 1

                i = 0

                while i < tamanho1:
                    teste3 += '<span>' + linha1[i:i+60] + '<br>' + linha2[i:i+60] + '<br>' + linha3[i:i+60] + '</span><br><br>'
                    i += 60
            else:
                teste3 = '<div>'
                linha1 = ''
                linha2 = ''
                linha3 = ''

                contador = 0

                while contador < len(sequencia2):
                    # print(contador)
                    linha1 += sequencia2[contador] 
                    
                    try:
                        if sequencia2[contador] == sequencia1[contador]:
                            linha2 += sequencia2[contador]
                        else: 
                            linha2 += '+'
                    except:
                        linha2 += ' '

                    try:
                        linha3 += sequencia1[contador]
                    except:
                        linha3 += ' '
                    
                    contador += 1

                i = 0

                while i < tamanho2:
                    teste3 += '<span>' + linha1[i:i+60] + '<br>' + linha2[i:i+60] + '<br>' + linha3[i:i+60] + '</span><br><br>'
                    i += 60

        dados = {
           'teste3': teste3,
        }

    return JsonResponse(dados)
        

    
def comparar(request):
    
    dados = {}

    if request.method == 'POST':
        if(request.POST.get('act') == 'teste'):

            sequencia1 = request.POST.get('sequencia1') 
            sequencia2 = request.POST.get('sequencia2') 

            tamanho1 = int(request.POST.get('tamanho1'))
            tamanho2 = int(request.POST.get('tamanho2'))
            
            comparacao1 = ''
            comparacaoM = ''
            comparacao2 = ''

            aminoacidos_seq1 = {'A': 0,'C': 0,'D': 0,'E': 0,'F': 0,'G': 0,'H': 0,'I': 0,'K': 0,'L': 0,'M': 0,'N': 0,'P': 0,'Q': 0,'R': 0,'S': 0,'T': 0,'V': 0,'W': 0,'Y': 0}
            aminoacidos_seq2 = {'A': 0,'C': 0,'D': 0,'E': 0,'F': 0,'G': 0,'H': 0,'I': 0,'K': 0,'L': 0,'M': 0,'N': 0,'P': 0,'Q': 0,'R': 0,'S': 0,'T': 0,'V': 0,'W': 0,'Y': 0}

            count = 0
            espaco = 0
            for i in sequencia1:
                if sequencia1[count] == ' ':
                    count += 1
                    espaco += 1
                    continue
                aminoacidos_seq1[i] = aminoacidos_seq1[i] + 1
                count += 1

            count = count - espaco
            
            tam_seq_1 = count

            aparicao_seq1 = '<div style="color: white;">' + '<b>Quantidade de Aparições para cada Amionoacido </b><br>A: '+  str(aminoacidos_seq1['A']) + ' C: '+ str(aminoacidos_seq1['C'])+ ' D: '+ str(aminoacidos_seq1['D'])+ ' E: '+ str(aminoacidos_seq1['E'])+ ' F: '+ str(aminoacidos_seq1['F'])+ ' G: '+ str(aminoacidos_seq1['G'])+ ' H: '+ str(aminoacidos_seq1['H'])+' I: '+ str(aminoacidos_seq1['I'])+ ' K: '+ str(aminoacidos_seq1['K'])+ ' L: '+ str(aminoacidos_seq1['L'])+ ' M: '+ str(aminoacidos_seq1['M'])+ ' N: '+ str(aminoacidos_seq1['N'])+ ' P: '+ str(aminoacidos_seq1['P'])+ ' Q: '+ str(aminoacidos_seq1['Q'])+ ' R: '+ str(aminoacidos_seq1['R'])+ ' S: '+ str(aminoacidos_seq1['S'])+ ' T: '+ str(aminoacidos_seq1['T'])+ '<br>V: '+ str(aminoacidos_seq1['V'])+ ' W: '+ str(aminoacidos_seq1['W'])+ ' Y: '+ str(aminoacidos_seq1['Y'])+' </div>'
            porc_seq1 = '<div style="color: white;">'+ '<b>Porcentagem de Aparições para cada Amionoacido </b><br>A: '+ str(round(aminoacidos_seq1['A'] * 100 / count, 2))+ '% C: '+ str(round(aminoacidos_seq1['C'] * 100 / count, 2))+ '% D: '+ str(round(aminoacidos_seq1['D'] * 100 / count, 2))+ '% E: '+ str(round(aminoacidos_seq1['E'] * 100 / count, 2))+ '% F: '+ str(round(aminoacidos_seq1['F'] * 100 / count, 2))+ '% G: '+ str(round(aminoacidos_seq1['G'] * 100 / count, 2))+ '% H: '+ str(round(aminoacidos_seq1['H'] * 100 / count, 2))+'% I: '+ str(round(aminoacidos_seq1['I'] * 100 / count, 2))+ '% K: '+ str(round(aminoacidos_seq1['K'] * 100 / count, 2))+ '% L: '+ str(round(aminoacidos_seq1['L'] * 100 / count, 2))+ '%<br>M: '+ str(round(aminoacidos_seq1['M'] * 100 / count, 2))+ '% N: '+ str(round(aminoacidos_seq1['N'] * 100 / count, 2))+ '% P: '+ str(round(aminoacidos_seq1['P'] * 100 / count, 2))+ '% Q: '+ str(round(aminoacidos_seq1['Q'] * 100 / count, 2))+ '% R: '+ str(round(aminoacidos_seq1['R'] * 100 / count, 2))+ '% S: '+ str(round(aminoacidos_seq1['S'] * 100 / count, 2))+ '% T: '+ str(round(aminoacidos_seq1['T'] * 100 / count, 2))+ '% V: '+ str(round(aminoacidos_seq1['V'] * 100 / count, 2))+ '% W: '+ str(round(aminoacidos_seq1['W'] * 100 / count, 2))+ '% Y: '+ str(round(aminoacidos_seq1['Y'] * 100 / count, 2))+'% </div>'
     
            count = 0

            for i in sequencia2:
                if sequencia2[count] == ' ':
                    count += 1
                    espaco += 1
                    continue
                aminoacidos_seq2[i] = aminoacidos_seq2[i] + 1
                count += 1
            
            count = count - espaco
            
            tam_seq_2 = count

            aparicao_seq2 = '<div style="color: white;">' + '<b>Quantidade de Aparições para cada Amionoacido </b><br>A: '+  str(aminoacidos_seq2['A']) + ' C: '+ str(aminoacidos_seq2['C'])+ ' D: '+ str(aminoacidos_seq2['D'])+ ' E: '+ str(aminoacidos_seq2['E'])+ ' F: '+ str(aminoacidos_seq2['F'])+ ' G: '+ str(aminoacidos_seq2['G'])+ ' H: '+ str(aminoacidos_seq2['H'])+' I: '+ str(aminoacidos_seq2['I'])+ ' K: '+ str(aminoacidos_seq2['K'])+ ' L: '+ str(aminoacidos_seq2['L'])+ ' M: '+ str(aminoacidos_seq2['M'])+ ' N: '+ str(aminoacidos_seq2['N'])+ ' P: '+ str(aminoacidos_seq2['P'])+ ' Q: '+ str(aminoacidos_seq2['Q'])+ ' R: '+ str(aminoacidos_seq2['R'])+ ' S: '+ str(aminoacidos_seq2['S'])+ ' T: '+ str(aminoacidos_seq2['T'])+ '<br>V: '+ str(aminoacidos_seq2['V'])+ ' W: '+ str(aminoacidos_seq2['W'])+ ' Y: '+ str(aminoacidos_seq2['Y'])+' </div>'
            porc_seq2 = '<div style="color: white;">'+ '<b>Porcentagem de Aparições para cada Amionoacido </b><br>A: '+ str(round(aminoacidos_seq2['A'] * 100 / count, 2))+ '% C: '+ str(round(aminoacidos_seq2['C'] * 100 / count, 2))+ '% D: '+ str(round(aminoacidos_seq2['D'] * 100 / count, 2))+ '% E: '+ str(round(aminoacidos_seq2['E'] * 100 / count, 2))+ '% F: '+ str(round(aminoacidos_seq2['F'] * 100 / count, 2))+ '% G: '+ str(round(aminoacidos_seq2['G'] * 100 / count, 2))+ '% H: '+ str(round(aminoacidos_seq2['H'] * 100 / count, 2))+'% I: '+ str(round(aminoacidos_seq2['I'] * 100 / count, 2))+ '% K: '+ str(round(aminoacidos_seq2['K'] * 100 / count, 2))+ '% L: '+ str(round(aminoacidos_seq2['L'] * 100 / count, 2))+ '%<br>M: '+ str(round(aminoacidos_seq2['M'] * 100 / count, 2))+ '% N: '+ str(round(aminoacidos_seq2['N'] * 100 / count, 2))+ '% P: '+ str(round(aminoacidos_seq2['P'] * 100 / count, 2))+ '% Q: '+ str(round(aminoacidos_seq2['Q'] * 100 / count, 2))+ '% R: '+ str(round(aminoacidos_seq2['R'] * 100 / count, 2))+ '% S: '+ str(round(aminoacidos_seq2['S'] * 100 / count, 2))+ '% T: '+ str(round(aminoacidos_seq2['T'] * 100 / count, 2))+ '% V: '+ str(round(aminoacidos_seq2['V'] * 100 / count, 2))+ '% W: '+ str(round(aminoacidos_seq2['W'] * 100 / count, 2))+ '% Y: '+ str(round(aminoacidos_seq2['Y'] * 100 / count, 2))+'% </div>'

            # print(aminoacidos_seq1)

            indice = 0
            count_amino = 1
            #for indice in range(len(sequencia)):
            if (tamanho1 > tamanho2):
                while indice < len(sequencia1):
                    # print(indice)
                    try:
                        if(sequencia1[indice] == sequencia2[indice]):
                            comparacao1 += '<span class="verde">'+sequencia1[indice]+'</span>'
                            try:
                                comparacao2 += '<span class="verde">'+sequencia2[indice]+'</span>'
                            except:
                                comparacao2 += '<span>-</span>'
                                
                        else:
                            comparacao1 += '<span class="vermelho">'+sequencia1[indice]+'</span>'
                            try:
                                comparacao2 += '<span class="vermelho">'+sequencia2[indice]+'</span>'
                            except:
                                comparacao2 += '<span>-</span>'

                        indice += 1
                    except:
                        comparacao1 += '<span class="vermelho">'+sequencia1[indice]+'</span>'
                        indice += 1
 
                    if count_amino % 60 == 0: 
                        comparacao1 += '<br>'
                        comparacao2 += '<br>'

                    count_amino += 1    

                    
            else:
                while indice < len(sequencia2):
                    try:
                        if(sequencia1[indice] == sequencia2[indice]):
                            comparacao2 += '<span class="verde">'+sequencia2[indice]+'</span>'
                            try:
                                comparacao1 += '<span class="verde">'+sequencia1[indice]+'</span>'
                            except:
                                comparacao1 += '<span>-</span>'

                        else:
                            comparacao2 += '<span class="vermelho">'+sequencia2[indice]+'</span>'
                            try:
                                comparacao1 += '<span class="vermelho">'+sequencia1[indice]+'</span>'
                            except:
                                comparacao1 += '<span>-</span>'

                        indice += 1
                    except:
                        comparacao2 += '<span class="vermelho">'+sequencia2[indice]+'</span>'
                        indice += 1
                    

                    if count_amino % 50 == 0:   
                        comparacao1 += '<br>'
                        comparacao2 += '<br>'

                    count_amino += 1

            teste3 = '<div>'
            linha1 = ''
            linha2 = ''
            linha3 = ''
            
            if tamanho1 > tamanho2:

                contador = 0

                while contador < len(sequencia1):
                    # print(contador)
                    linha1 += sequencia1[contador] 
                    
                    try:
                        if sequencia1[contador] == sequencia2[contador]:
                            linha2 += sequencia1[contador]
                        else: 
                            linha2 += '+'
                    except:
                        linha2 += ' '

                    try:
                        linha3 += sequencia2[contador]
                    except:
                        linha3 += ' '
                    
                    contador += 1

                i = 0
                while i < tamanho1:
                    teste3 += '<span>' + linha1[i:i+60] + '<br>' + linha2[i:i+60] + '<br>' + linha3[i:i+60] + '</span><br><br>'
                    i += 60

            else:

                contador = 0

                while contador < len(sequencia2):
                    # print(contador)
                    linha1 += sequencia2[contador] 
                    
                    try:
                        if sequencia2[contador] == sequencia1[contador]:
                            linha2 += sequencia2[contador]
                        else: 
                            linha2 += '+'
                    except:
                        linha2 += ' '

                    try:
                        linha3 += sequencia1[contador]
                    except:
                        linha3 += ' '
                    
                    contador += 1           

                i = 0

                while i < tamanho2:
                    teste3 += '<span>' + linha1[i:i+60] + '<br>' + linha2[i:i+60] + '<br>' + linha3[i:i+60] + '</span><br><br>'
                    i += 60


            html = "\
            <div>\
                <h4> Resultados </h4>\
                <b>Teste</b>\
            </div>\
            "

            dados = {
                'seq1': request.POST.get('sequencia1'),
                'seq2': request.POST.get('sequencia2'),
                'comparacao1': comparacao1,
                'comparacao2': comparacao2,
                'teste3': teste3,
                'aminoacidos1': aminoacidos_seq1,
                'aminoacidos2': aminoacidos_seq2,
                'aparicao': aparicao_seq1,
                'porcentagem': porc_seq1,
                'aparicao2': aparicao_seq2,
                'porcentagem2': porc_seq2,
                'tamanho': tam_seq_1,
                'tamanho2': tam_seq_2
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
            
            #print(seq_aminoacidos)
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
    



def Alinhamento(request):
    dados = {}
    if request.method == 'POST':

        sequencia1 = request.POST.get('sequencia1') 
        sequencia2 = request.POST.get('sequencia2') 

        tamanho1 = int(request.POST.get('tamanho1'))
        tamanho2 = int(request.POST.get('tamanho2'))  
        
        if tamanho1 > tamanho2:
            teste3 = '<div>'
            linha1 = ''
            linha2 = ''
            linha3 = ''

            contador = 0

            while contador < len(sequencia1):
                # print(contador)
                linha1 += sequencia1[contador] 
                
                try:
                    if sequencia1[contador] == sequencia2[contador]:
                        linha2 += sequencia1[contador]
                    else: 
                        linha2 += '+'
                except:
                    linha2 += ' '

                try:
                    linha3 += sequencia2[contador]
                except:
                    linha3 += ' '
                
                contador += 1

            i = 0

            while i < tamanho1:
                teste3 += '<span>' + linha1[i:i+60] + '<br>' + linha2[i:i+60] + '<br>' + linha3[i:i+60] + '</span><br><br>'
                i += 60

            dados = {
                'teste3': teste3,
            }

    return JsonResponse(dados)