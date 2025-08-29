from django.contrib import admin
from .models import Team, Fixture

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Configuración del Admin para los Equipos.
    """
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    """
    Configuración del Admin para los Partidos (Fixtures).
    """
    list_display = ('display_order', '__str__', 'category', 'match_datetime')
    list_filter = ('category', 'match_datetime', 'home_team', 'away_team', 'tournament_name')
    # Le decimos a Django que la columna de enlace es la que muestra el texto del partido
    list_display_links = ('__str__',) 
    search_fields = ('home_team__name', 'away_team__name', 'venue', 'tournament_name', 'stage')
    autocomplete_fields = ('home_team', 'away_team')
    # Esta línea te permite editar el orden directamente desde la lista
    list_editable = ('display_order',)
    
    fieldsets = (
        (None, {
            'fields': (('home_team', 'away_team'), ('home_score', 'away_score'), 'category')
        }),
        ('Detalles del Partido', {
            'fields': ('match_datetime', 'venue', 'league_name', 'tournament_name', 'stage', 'display_order')
        }),
    )

    def get_changeform_initial_data(self, request):
        """
        Define los datos iniciales para el formulario de creación.
        """
        try:
            # Busca el equipo llamado 'Olimpo'. Asegúrate de que exista en tu base de datos.
            olimpo_team = Team.objects.get(name__iexact="Olimpo")
            return {'home_team': olimpo_team}
        except Team.DoesNotExist:
            # Si no encuentra a 'Olimpo', no hace nada para evitar un error.
            return {}
