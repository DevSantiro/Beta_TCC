from django import forms

from .models import DNA, Proteina

class DNAForm(forms.ModelForm):
    
    class Meta:
        model = DNA
        fields = ('titulo','cabecalho', 'sequencia')


class ProtForm(forms.ModelForm):
    
    class Meta:
        model = Proteina 
        fields = ('titulo','cabecalho', 'sequencia')

