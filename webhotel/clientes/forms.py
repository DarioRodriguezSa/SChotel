from django import forms
from .models import  genero
      
class GeneroForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre del género",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = genero
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(GeneroForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Género"



