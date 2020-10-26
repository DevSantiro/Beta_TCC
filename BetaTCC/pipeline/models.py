from django.db import models

# Create your models here.

class Modelos(models.Model):
    diretorio = models.CharField(max_length=255)    
    
    def __str__(self):
        return self.diretorio


class Arquivos(models.Model):
    diretorio_modelo = models.ForeignKey(
        Modelos, on_delete=models.CASCADE)
    arquivo = models.CharField(max_length=255)  
    extensao = models.CharField(max_length=255) 
    id_diretorio = models.IntegerField()

    def __str__(self):
        return self.arquivo

