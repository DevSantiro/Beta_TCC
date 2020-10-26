from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import JsonResponse
from django.core.files.uploadedfile import UploadedFile
from django import forms
from Bio.PDB import Polypeptide
import os
import subprocess
from .models import *
import sqlite3

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


class testeFormulario(forms.Form):
    proteina   = forms.Textarea()
    arquivo    = forms.Textarea()

# Classe conexao banco de dados sqlite3
class conexaoBanco:

    @staticmethod
    def criaARVBanco():
        path = 'db.sqlite3'

        conn = sqlite3.connect(path)
        conn.close()

class Banco:  
    path = 'db.sqlite3'

    def conectaBanco(self):
        conn = sqlite3.connect(self.path)
        print ('Aberta a Conexão')
        return conn
    
    def fechaBanco(self,conn):
        conn.close()
        print('Conexão Fechada')

    def getDiretorioID(self, idx):
        
        conecta = Banco()
        
        conn = conecta.conectaBanco()
        
        cursor = conn.cursor()   

        query = "SELECT diretorio FROM modelos WHERE id = " + str(idx)

        cursor.execute(query)

        diretorios = cursor.fetchall()

        # editar diretorio

        diretorio = 'arquivos_'+str(diretorios[0][0])
        
        return diretorio


    def getDiretorios(self):
    
        conecta = Banco()
        
        conn = conecta.conectaBanco()
        
        cursor = conn.cursor()   

        query = "SELECT * FROM modelos"

        cursor.execute(query)

        diretorios = cursor.fetchall()
        
        return diretorios

    def cadastraModelo(self,nome):
        
        conecta = Banco()
        
        conn = conecta.conectaBanco()
        
        cursor = conn.cursor()        
        
        #Altere para os valores necessarios a sua tabela
        
        query_insert = "INSERT INTO modelos (diretorio) VALUES ('"+ nome +"')"
        
        # insert_values = (nome)
        
        cursor.execute(query_insert)
        
        cursor.execute('SELECT MAX(id) FROM modelos')
            
        maxid = cursor.fetchall()

        conn.commit()
        
        return maxid[0][0]

    def getArquivosID(self, idmodelo):

        conecta = Banco()
        
        conn = conecta.conectaBanco()
        
        cursor = conn.cursor() 

        query = "select arquivo, extensao from arquivos where extensao like '%pdb' and id_modelo = " + str(idmodelo)

        cursor.execute(query)

        arquivos = cursor.fetchall()

        #print(arquivos)

        return arquivos



    def cadastraArquivo(self, id_modelo, array): 

        conecta = Banco()
        
        conn = conecta.conectaBanco()
        
        cursor = conn.cursor()        
        
        #Altere para os valores necessarios a sua tabela

        for arquivo in array:
            
            separador = arquivo.split('.')

            extensao = separador[1:]

            print(separador[0])

            novo = ''

            tamanho = len(extensao)
            count = 1

            for ext in extensao:
                if tamanho > count:
                    novo += ext+"."
                else:
                    novo += ext

                count += 1

            query_insert = "INSERT INTO arquivos (id_modelo, arquivo, extensao) VALUES ("+ str(id_modelo) +", '" + separador[0] + "', '"+ novo +"')"
                        
            cursor.execute(query_insert)
            
            conn.commit()
        
        return 1




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

        # Cadeia da Sequencia
        cadeiaS = request.POST.get('cadeiaS').upper()

        #Cadeia do Template
        cadeiaT = request.POST.get('cadeiaT').upper()

        fs = FileSystemStorage()
        
        fs.save(proteina.name, proteina)
        fs.save(template.name, template)
        
        w = open("media\\"+ template.name +".fasta","w")
        w.write(">"+template.name+"\n")
        cadeia = cadeiaT # Aqui eu estou deixando Fixo "A", mas no caso não é o correto, deveria verificar uma forma de identificar. Cadeia Template * Update 23/09
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
                    new_aln.write("sequence:"+proteina.name+":"+str(1)+":"+str(cadeiaS)+":"+str(tamanho_seq)+":"+str(cadeiaS)+"::::") # Mesma coisa aqui, porém aqui é a Cadeia da Sequencia que vamos modelar!
            else:
                new_aln.write(linha)
        new_aln.close()
        seq.close()
        # ****************************************************************************************
        # modeller
        # ****************************************************************************************
        criaScript(proteina, template)

        os.system("media\\Modeller.lnk")

        # Atualizar o arquivo.bat dinamico para ir de acordo com a pasta  


        atualizaArquivoBAT(proteina.name)
        max_id = inserirDiretorio(proteina.name)

        os.system("media\\clear.lnk")

        inserirArquivos(proteina.name, max_id)

        d = Banco()

        diretorios = d.getDiretorios()

        print(diretorios[0][0])

        # result = subprocess.run(['dir', '*.py'], stdout=subprocess.PIPE)
        # result.stdout

        # print(result.stdout)    
        return render(request, 'pipeline/upload.html', {'resultado': '1', 'diretorios': diretorios[0:] } ) # Falta aqui! 


    d = Banco()

    diretorios = d.getDiretorios()

    #print(diretorios[0][0])
    
    # listaUL = '<ul class="prot-list">'
    # contador = 0

    # for dire in diretorios:

    #     listaUL += '<li class="prot-item"><span><a href="">'+ dire[contador][contador] +'</a></span></li>'
    #     contador += 1
    
    # listaUL += '</ul>'

    return render(request, 'pipeline/upload.html')

    

def gerarLista(request):
    #pass
    
    d = Banco()

    diretorios = d.getDiretorios()

    listaUL = ''

    for dire in diretorios:
        # print(type(dire[0]))

        nome = dire[0]
        idm = dire[1]
        print(nome)
        listaUL += '<li class="prot-item"><span><a href="/pipeline/Modelos/'+ str(idm) +'">'+ nome +'</a></span></li>'
    
           
    dados = {'listaUL': listaUL}

    return JsonResponse(dados)

def criaScript(template, proteina):
    w = open("media\\run.py","w")
    script = "from modeller import *\nfrom modeller.automodel import *\nlog.verbose()\nenv = environ()\n\nenv.io.atom_files_directory = ['\\modelos']\n\nenv.io.hetatm = True\nenv.io.water = True\n\na = automodel(env, alnfile = 'new_alinha.pir', knowns = '"+proteina.name+"', sequence = '"+template.name+"')\na.starting_model = 1\na.ending_model = 2\na.make() \n"
    w.write(script)
    w.close()
    
# Implementar uma Rotina para tentar pegar toda a sequencia inserida e começar a execução do Pipeline

def organizaDiretorio():
    os.system('mkdir \\media ')
    pass



def get_arquivos(*args):
    arquivos = []
    for item in args:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                arquivos.append((file))
    return arquivos


def atualizaArquivoBAT(nome):
    arquivo = open("media\\clear.bat", "w")
    # arquivo.write('mkdir ', proteina.name ,')
    arquivo.write('mkdir arquivos_'+ str(nome) +' \n')
    arquivo.write('move *.pdb arquivos_'+ str(nome) +' \n')
    arquivo.write('move *.pir arquivos_'+ str(nome) +' \n')
    arquivo.write('move *.fasta arquivos_'+ str(nome) +'\n')
    arquivo.write('move *.log arquivos_'+ str(nome) +'\n')
    arquivo.write('del *.dnd \n')
    arquivo.write('del *.fasta.* \n')
    arquivo.write('del *run.py \n')
    arquivo.write('exit \n')
    arquivo.close()


def inserirDiretorio(nome):

    d = Banco()
    max_id = d.cadastraModelo(nome)


    return max_id


def inserirArquivos(nome, max_id):

    d = Banco()

    diretorio = 'media\\arquivos_'+str(nome)

    array = get_arquivos(diretorio)

    print(diretorio)
    print(array)
    print(max_id)

    d.cadastraArquivo(max_id, array)


def Modelos(request, id):

    # if request.method == 'POST':
    d = Banco()

    diretorio = d.getDiretorioID(id)

    html = '{% extends "modelagem/base.html" %} {% block body %} {% load static %} <div id="info_loading" style="padding-top: 10px;" class="alert alert-warning" role="alert"><span style="font-size:28px; font-weight: bold; widht: 50%;" id="header-info"><i id="icon" style="font-size: 28px;" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i> Carregando...</span><span id="btn-voltar" style="float: right; widht: 50%; display: none;"> <button class="btn btn-primary" onclick="Botao_voltar()">Voltar</button></span></div><div class="invi" style="width: 100%;"><input type="text" id="valor_scroll" value="0" hidden>'

    diretorio = 'media\\'+str(diretorio)

    array = get_arquivos(diretorio)

    #print(array)

    arquivos = d.getArquivosID(id)


    # Criando Lista de Arquivos e juntando a extensao

    listaArq = []
    # conteudoArq = []
    teste = ''
    for arq in arquivos:
        arq_new = arq[0] + '.' + arq[1]
        listaArq.append(arq_new)

    #     atual = open(diretorio + '\\' + arq_new, "r")
    #     # conteudoArq.append(atual.readlines())
    #     teste = str(atual.readlines())
    #     atual.close()
        
    # teste = teste.replace("['", "")
    # teste = teste.replace("']", "")
    # teste = teste.replace("',", "")
    # teste = teste.replace("'", "")






    contador = 1
    # arquivo_cont = 0
    for arq in listaArq:

        html += '<div style="height: 300px; background-color: white;"><div style="width: 400px; float: left;"><div class="modelo3d" id="viewport'+ str(contador) +'" style="width:400px; height:300px;"></div></div><div style="background-color: white; width: 70%; float:right;"><b style="font-size: 28px";>Modelo: <span style="color:blue;">'+ str(arq) +'</span> Score: <span style="color:green;" id="score'+ str(contador) +'"> </span></b> <textarea disabled style="width: 100%;" rows="7" cols="50" name="" disabled id="modelo'+ str(contador) +'" data-modelo='+str(arq)+'>Realizando a leitura do Arquivo...\nAguarde um momento...</textarea> <button  class="block btn btn-secondary" onclick="Bloquear();"><i class="fa fa-lock" aria-hidden="true"></i> Bloquear Scroll</button> <button class="btn btn-primary" onclick="Download('+ str(contador) +');" ><i class="fa fa-download"></i> Download Arquivo</button> </div></div>'

        contador += 1
        # arquivo_cont += 1

    html += '</div>'
    contador -= 1
    # qnt = '<input type="text" id="aux_qnt" value='+ str(contador) +' hidden>'



    #Script dinamico
    i = 1
    
    variaveis = ''
    script = ''
    eventoWindow = ''
    loadFile = ''
    download = ''
    ajax = ''
    btn_voltar = ''
    script = 'document.addEventListener("DOMContentLoaded", function () {'
    eventoWindow = 'window.addEventListener("resize", function (event) {'
    while i <= contador:
        variaveis += 'var stage' + str(i) + ' = new NGL.Stage("viewport'+str(i)+'");'
        eventoWindow += 'stage' + str(i) + '.handleResize();'
        i += 1

    eventoWindow += '}, false);'

    # Ajax para carregar conteudo arquivos
    ajax = '$.ajax({method: "POST",url: "/pipeline/lerArquivos/'+str(id)+'" , dataType: "json", data: { csrfmiddlewaretoken: "{{csrf_token}}"  },success: function(data){ for(i = 1; i <= data["quantidade"]; i++){ $("#modelo"+i).html(data["modelo"+i]); if(i == 1){ $("#score"+i).html("Template - Sem Score") }else { $("#score"+i).html(data["score"+i]); } } $("#icon").removeClass("fa fa-spinner fa-pulse fa-3x fa-fw"); $("#info_loading").removeClass("alert-warning").addClass("alert-info"); $("#header-info").html("Carregado com Sucesso!"); $("#btn-voltar").css("display", "block"); }  });  '

    # Mudando o diretorio para funcionar dinamicamente
    
    diretorio = diretorio.replace("\\", "//")

    contador = 1
    for arq in listaArq:
        loadFile += 'stage'+ str(contador) +'.loadFile("/'+str(diretorio)+'/'+str(arq)+'", { defaultRepresentation: true });'
        contador += 1
    loadFile += '});'


    # Mudando o diretorio para funcionar com Java Script
    diretorio = diretorio.replace("//", "/")


    download = 'function Download(modelo){ var modelo_3d = $("#modelo"+modelo).data("modelo"); var diretorio = "/'+str(diretorio)+'/"+modelo_3d;  window.open(diretorio); }'

    btn_voltar = 'function Botao_voltar(){ window.location.href = "/pipeline/upload";  }'

    # window.open("/'+str(diretorio)+'");

    script +=  variaveis + eventoWindow + loadFile + download + ajax + btn_voltar

    # print(script)

    # print(variaveis)
    # print(eventoWindow)
    # print(loadFile)

    html += '<script>'

    html += 'function Bloquear(){var acao = $("#valor_scroll").val();if(acao == 0){$("html").css("overflow", "hidden");$("#valor_scroll").val("1");$(".block").html("Desbloquear Scroll"); }else{$("html").css("overflow", "");$("#valor_scroll").val("0");   $(".block").html("Bloquear Scroll");} }'

    html += script + '</script> {% endblock %}'

    w = open("pipeline\\templates\\pipeline\\teste.html","w")
    w.write(html)
    w.close()

    return render(request, 'pipeline/teste.html')


def lerArquivos(request, id):
    if request.method == 'POST':

        d = Banco()
        diretorio = d.getDiretorioID(id)
            
        diretorio = 'media\\'+str(diretorio)
        array = get_arquivos(diretorio)                

        arquivos = d.getArquivosID(id)

        contador = 1
        
        dados = {}

        for arq in arquivos:
            arq_new = arq[0] + '.' + arq[1]

            conteudo_arquivo = open(diretorio + '\\' + str(arq_new), 'r')
            linhas_arquivo = conteudo_arquivo.readlines()
            conteudo_arquivo.close()

            # conteudo do arquivo vira valor do dicionario
            valor_dicionario = linhas_arquivo
            valor_score = str(linhas_arquivo[1][45:])

            # chave_valor = "'modelo"+str(contador)+"': "+ str(valor_dicionario)

            dados['modelo'+str(contador)] = valor_dicionario
            dados['score'+str(contador)] = valor_score

            # lista_dicionario.append(chave_valor)
            contador += 1

        dados['quantidade'] = str(len(arquivos))

        return JsonResponse(dados)
        

