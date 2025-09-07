from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    """
    Formulario para crear y editar Álbumes.
    """
    class Meta:
        model = Album
        fields = ['title', 'description']
        labels = {
            'title': 'Título del Álbum',
            'description': 'Descripción (Opcional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }