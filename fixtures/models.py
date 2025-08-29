from django.db import models
from players.models import Category # Importamos el modelo Category de nuestra app 'players'

class Team(models.Model):
    """Representa un equipo de fútbol, ya sea el nuestro o un rival."""
    name = models.CharField("Nombre del Equipo", max_length=150, unique=True)
    shield_image = models.ImageField("Escudo", upload_to='team_shields/', blank=True, null=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ['name']

    def __str__(self):
        return self.name

class Fixture(models.Model):
    """Representa un único partido del fixture."""
    # --- Información del Partido ---
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_fixtures", verbose_name="Equipo Local")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_fixtures", verbose_name="Equipo Visitante")
    
    home_score = models.PositiveIntegerField("Goles Local", null=True, blank=True)
    away_score = models.PositiveIntegerField("Goles Visitante", null=True, blank=True)
    
    match_datetime = models.DateTimeField("Fecha y Hora del Partido", null=True, blank=True)
    venue = models.CharField("Estadio o Lugar", max_length=150, blank=True)
    
    # --- Información Adicional del Torneo ---
    league_name = models.CharField("Nombre de la Liga", max_length=150, blank=True)
    tournament_name = models.CharField("Nombre del Torneo", max_length=150, blank=True)
    stage = models.CharField("Etapa del Torneo", max_length=100, blank=True) # Ej: "Fecha 1", "Semifinal"
    
    # Vinculamos el partido a una de las categorías de nuestro club
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="fixtures", verbose_name="Categoría del Club")

    display_order = models.PositiveIntegerField("Orden", default=0, help_text="Menor número aparece primero")

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        ordering = ['display_order', 'match_datetime']

    def __str__(self):
        # Primero, verificamos si hay una fecha y creamos el texto correspondiente
        date_str = self.match_datetime.strftime('%d/%m/%Y') if self.match_datetime else 'Fecha a definir'
        
        # Luego, construimos la cadena de texto final
        return f"{self.home_team} vs {self.away_team} ({self.category.name}) - {date_str}"