from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import JsonResponse
from django.core.files.uploadedfile import UploadedFile
from django import forms
from Bio.PDB import Polypeptide
import os
import subprocess

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


class testeFormulario(forms.Form):
    proteina   = forms.Textarea()
    arquivo    = forms.Textarea()

# Create your views here.

def lerArquivos(request):
    if request.method == 'POST':
        
        arquivo = open('media\\4hpg.pdb', 'r')
        lista = arquivo.readlines() # readlinesssssss
        arquivo.close()

        arquivo = open('media\\beta_glucosidase.fasta.B99990001.pdb', 'r')
        modelo = arquivo.readlines() # readlinesssssss
        arquivo.close()

        arquivo = open('media\\beta_glucosidase.fasta.B99990002.pdb', 'r')
        modelo1 = arquivo.readlines() # readlinesssssss
        arquivo.close()

        arquivo = open('media\\beta_glucosidase.fasta.B99990003.pdb', 'r')
        modelo2 = arquivo.readlines() # readlinesssssss
        arquivo.close()

        dados = {'teste': lista,
                 'modelo': modelo,           
                 'modelo1': modelo1,           
                 'modelo2': modelo2           
                }
        # print(lista)
        return JsonResponse(dados)


def Index(request):
    
    return render(request, 'pipeline/teste.html') 

def Teste(request):
    
    return render(request, 'pipeline/index.html') 

# Metodo oficial para gerar a modelagem (Pipeline)
def upload(request):
    # Processo Pipeline concluido - Falta somente pegar o melhor modelo gerado.
    # Rodrigo 27/07/2020.
    
    if request.method == 'POST':
        
        #diretorio = ""

        proteina = request.FILES['proteina']
        template = request.FILES['documento']

        fs = FileSystemStorage()
        
        fs.save(proteina.name, proteina)
        fs.save(template.name, template)
        
        w = open("media\\"+ template.name +".fasta","w")
        w.write(">"+template.name+"\n")
        cadeia = 'A' # Aqui eu estou deixando Fixo "A", mas no caso não é o correto, deveria verificar uma forma de identificar.
        comeco = 0
        fim = 0
        pdb = open('media\\' + template.name).readlines()
        for linha in pdb:
            if linha[0:4] == "ATOM" and linha[21] == cadeia and linha[13:15] == 'CA': # ver o que é CA
                resname3 = linha[17:20]
                if comeco == 0:
                    comeco = int(linha[22:26])
                if int(linha[22:26]) > fim:
                    fim = int(linha[22:26])
                resname1 = Polypeptide.three_to_one(resname3)
                w.write(resname1)
        w.write("\n")
        w.close()
        os.system("type media\\"+template.name+".fasta > media\\alinha.fasta")
        os.system("type media\\"+proteina.name+" >> media\\alinha.fasta")
        
        # run clustal-w
        os.system("clustalw2 -infile=media\\alinha.fasta -output=pir")
        #subprocess.call(["clustalw2.exe", "-infile='media\\alinha.fasta' -output='pir'"])
        aln = open("media\\alinha.pir").readlines()
        new_aln = open("media\\new_alinha.pir","w")
        tipo = 0 #0 = PDB; 1 = SEQ
        seq = open("media\\" + proteina.name)
        seq_final = ""
        for linha in seq:
            if linha[0] != ">":
                seq_final += linha.strip()
        tamanho_seq = len(seq_final)
        print("tamanho da seq = "+str(tamanho_seq))
        for linha in aln:
            if linha[0] == ">":
                if tipo == 0 and linha != "\n":
                    new_aln.write(">P1;"+template.name+"\n")
                    new_aln.write("structure:"+template.name+":"+str(comeco)+":"+cadeia+":"+str(fim)+":"+cadeia+"::::\n")
                    tipo = tipo+1
                elif tipo == 1:
                    new_aln.write(">P1;"+proteina.name+"\n")
                    new_aln.write("sequence:"+proteina.name+":"+str(1)+":A:"+str(tamanho_seq)+":A::::") # Mesma coisa aqui!
            else:
                new_aln.write(linha)
        new_aln.close()

        # ****************************************************************************************
        # modeller
        # ****************************************************************************************
        criaScript(proteina, template)

        os.system("media\\Modeller.lnk")
    
        return render(request, 'pipeline/upload.html', {'resultado': '1' } )
    
    return render(request, 'pipeline/upload.html' )
    


def criaScript(template, proteina):
    w = open("media\\run.py","w")
    script = "from modeller import *\nfrom modeller.automodel import *\nlog.verbose()\nenv = environ()\n\nenv.io.atom_files_directory = ['\\modelos']\n\nenv.io.hetatm = True\nenv.io.water = True\n\na = automodel(env, alnfile = 'new_alinha.pir', knowns = '"+proteina.name+"', sequence = '"+template.name+"')\na.starting_model = 1\na.ending_model = 3\na.make() \n"
    w.write(script)
    w.close()
    
# Implementar uma Rotina para tentar pegar toda a sequencia inserida e começar a execução do Pipeline



# A Fazeres: 

#  Observações sobre esse tipo de implementação:
#  Aqui eu consegui gerar uma função que recebe o arquivo enviado por 'POST' e pegar o conteúdo do arquivo enviado! 
#  No entando eu precisei utilizar um formulário (preciso verificar e adaptar melhor o uso do mesmo) UploadFileForm.
#  Ainda não está da forma que eu quero, mas já é um bom esboço para implementar a ideia do projeto.
#  É importante lembrar que apesar de conseguir ler o conteúdo, existem vários pequenos problemas, como os caracteres "\r" e "\n" (pesquisar para que serve "\r")
#  PS: optei por não armazenar os arquivos enviados por upload em um diretório (por enquanto), somente para evitar lixo eletrônico.

# Agora preciso trabalhar melhor com os valores obtidos através de um arquivo disparado direto da página, por "padrão", vou tentar considerar
# somente arquivos do tipo ".fasta", facilitando o trabalho. 
# Preciso ignorar o header (1º Linha do arquivo), o mesmo começa com um caractere de ">", podendo ser um identificador para remoção caso a 1º linha
# contenha.


# Rodrigo - 15/07/2020