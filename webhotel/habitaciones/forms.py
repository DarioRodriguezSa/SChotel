from django import forms
from .models import  estado, categoria
      
class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre de la Categoria",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = categoria
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Categoria"


class EstadoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre del Estado",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = estado
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(EstadoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Estado"






