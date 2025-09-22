from django import forms
from .models import Team, Fixture

class TeamForm(forms.ModelForm):
    """
    Formulario para crear y editar Equipos.
    """
    class Meta:
        model = Team
        fields = ['name', 'shield_image']
        labels = {
            'name': 'Nombre del Equipo',
            'shield_image': 'Escudo del Equipo (Opcional)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FixtureForm(forms.ModelForm):
    """
    Formulario para crear y editar Partidos.
    """
    class Meta:
        model = Fixture
        fields = [
            'home_team', 'away_team', 'home_score', 'away_score', 'category',
            'match_datetime', 'venue', 'league_name', 'tournament_name',
            'stage', 'display_order', 'is_featured'
        ]
        widgets = {
            'match_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'home_team': forms.Select(attrs={'class': 'form-select'}),
            'away_team': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'league_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tournament_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stage': forms.TextInput(attrs={'class': 'form-control'}),
            'home_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'away_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }