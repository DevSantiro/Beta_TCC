from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def Index(request):
    
    return render(request, 'pipeline/index.html') 

# Metodo teste para pegar o arquivo enviado pelo Formulário
# Também será necessário configurar o MEDIA_ROOT e MEDIA_URL em settings.py
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request, 'pipeline/upload.html')