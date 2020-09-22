from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.Index, name='teste'),
    path('upload', views.upload, name='upload'),
    path('2', views.Teste, name='2'),
    path('teste', views.lerArquivos, name='teste')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)