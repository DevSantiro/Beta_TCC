from django import forms

class Sequencia(forms.Form):
    nome = forms.CharField(max_length=100)
    sequencia = forms.CharField(max_length=1000)