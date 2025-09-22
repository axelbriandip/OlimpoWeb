from django import forms
from .models import TimelineEvent

class TimelineEventForm(forms.ModelForm):
    """
    Formulario para crear y editar Hitos de la historia.
    """
    class Meta:
        model = TimelineEvent
        fields = ['year', 'title', 'description', 'image', 'parent', 'exact_date']
        labels = {
            'year': 'Año del Evento',
            'title': 'Título del Hito',
            'description': 'Descripción',
            'image': 'Imagen (Opcional)',
            'parent': 'Hito Padre (si es un sub-hito)',
            'exact_date': 'Fecha Exacta (Opcional)',
        }
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'exact_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que la lista de Hitos Padre solo muestre los que no son sub-hitos
        # y excluimos al propio hito que se está editando para evitar bucles.
        queryset = TimelineEvent.objects.filter(parent__isnull=True)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        self.fields['parent'].queryset = queryset