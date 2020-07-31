from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listaProteina', views.listaProteina, name='Lista'),
    path('infoProteina/<int:id>', views.infoProteina, name='infoProteina'),
]
