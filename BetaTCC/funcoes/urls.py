from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index-funcao'),
    path('index', views.Index, name='index-funcoes'),
    path('comparar', views.comparar, name='comparar'),
    path('formulario', views.formulario, name="formulario")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)