from django.db import models

# Create your models here.

class Proteina(models.Model):
    titulo = models.CharField(max_length=255)
    cabecalho = models.CharField(max_length=255)
    sequencia = models.TextField()
    
    def __str__(self):
        return self.titulo

class DNA(models.Model):
    titulo = models.CharField(max_length=255)
    cabecalho = models.CharField(max_length=255)
    sequencia = models.TextField()
    
    def __str__(self):
        return self.titulo