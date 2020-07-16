from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()


class testeFormulario(forms.Form):
    proteina   = forms.Textarea()
    arquivo    = forms.Textarea()

# Create your views here.

def Index(request):
    
    return render(request, 'pipeline/index.html') 

# Metodo teste para pegar o arquivo enviado pelo Formulário
# Também será necessário configurar o MEDIA_ROOT e MEDIA_URL em settings.py
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        
        fs.save(uploaded_file.name, uploaded_file)
        
        caminho = fs.open(uploaded_file.name, 'r')
        
        conteudo = File(caminho)
        
        print(conteudo)

    return render(request, 'pipeline/upload.html')


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


def upload2(request):
    if request.method == 'POST':
        
        form = UploadFileForm(request.POST, request.FILES)


        file = request.FILES['proteina']
        arquivo = request.FILES['documento']

        data = file.read()

        data2 = arquivo.read()

        print(data)

        print(data2)

        # uploaded_file = request.FILES['document']
        # fs = FileSystemStorage()

        # fs.save(uploaded_file.name, uploaded_file)

        # uploaded = UploadedFile.read()

        # print(uploaded)


        

    return render(request, 'pipeline/upload.html')




def teste(request):
    if request.method == 'POST':
        form = testeFormulario(request.POST)
        if form.is_valid():
            proteina = request.POST['proteina']
            arquivo = request.POST['arquivo']

        print(proteina)
        print(arquivo)
        proteina = proteina.replace('\n','')
        print(len(proteina.replace(' ','')))
    return render(request, 'pipeline/teste.html')
    
# Implementar uma Rotina para tentar pegar toda a sequencia inserida e começar a execução do Pipeline
