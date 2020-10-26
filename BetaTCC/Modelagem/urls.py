from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('listaProteina', views.listaProteina, name='ListaProteina'),
    path('listaDNA', views.listaDNA, name='listaDNA'),
    path('selecionarTipo', views.selecionarTipo, name='selecao'),
    path('infoProteina/<int:id>', views.infoProteina, name='infoProteina'),
    path('infoDNA/<int:id>', views.infoDNA, name='infoDNA'),
    path('conversor', views.conversorDNA, name='conversor'),
    path('view3d', views.view3d, name='view3d'),
    path('newbutton/', views.newButton, name="new-button")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)