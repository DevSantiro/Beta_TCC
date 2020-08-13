from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listaProteina', views.listaProteina, name='ListaProteina'),
    path('listaDNA', views.listaDNA, name='listaDNA'),
    path('selecionarTipo', views.selecionarTipo, name='selecao'),
    path('infoProteina/<int:id>', views.infoProteina, name='infoProteina'),
    path('infoDNA/<int:id>', views.infoDNA, name='infoDNA'),
    path('conversor', views.conversorDNA, name='conversor')
]
