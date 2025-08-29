from django.db import models
from django.utils import timezone

class Category(models.Model):
    """Representa una categoría del club, ej: 'Sub-15', 'Primera'."""
    name = models.CharField("Nombre", max_length=100, unique=True)
    order = models.PositiveIntegerField("Orden", default=0, help_text="Menor número aparece primero")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Player(models.Model):
    """Representa a un único jugador del club."""    
    # --- Atributos Esenciales ---
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)
    photo = models.ImageField("Foto", upload_to='players/', blank=True, null=True)
    date_of_birth = models.DateField("Fecha de Nacimiento")
    birth_city = models.CharField("Ciudad de Nacimiento", max_length=100, blank=True)
    birth_province = models.CharField("Provincia de Nacimiento", max_length=100, blank=True)
    
    # --- Atributos Deportivos ---)
    bio = models.TextField("Biografía", blank=True)
    join_date = models.DateField("Fecha de Ingreso", default=timezone.now)
    class PlayerPosition(models.TextChoices):
        ARQUERO = 'Arquero', 'Arquero'
        DEFENSOR = 'Defensor', 'Defensor'
        MEDIOCAMPISTA = 'Mediocampista', 'Mediocampista'
        DELANTERO = 'Delantero', 'Delantero'
        DIRECTOR_TECNICO = 'Director Técnico', 'Director Técnico'
        AYUDANTE_DE_CAMPO = 'Ayudante de Campo', 'Ayudante de Campo'
        PREPARADOR_FISICO = 'Preparador Físico', 'Preparador Físico'
    
    position = models.CharField(
        "Posición",
        max_length=50,
        choices=PlayerPosition.choices, # Asignamos las opciones al campo
        blank=True
    )

    # --- Atributos Administrativos (Privados) ---
    dni = models.CharField("DNI", max_length=20, blank=True)
    member_id = models.CharField("Número de Socio", max_length=50, blank=True)
    is_active = models.BooleanField("Está Activo", default=True) # Para borrados suaves

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    managed_categories = models.ManyToManyField(
            Category,
            verbose_name="Categorías a Cargo",
            blank=True, # Es opcional, ya que solo aplica al cuerpo técnico
            related_name="coaching_staff"
        )

    @property
    def age(self):
        """Calcula la edad actual del jugador."""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    # --- ESTA ES LA PROPIEDAD QUE FALTABA ---
    @property
    def age_category(self):
        """Calcula la categoría de edad dinámica (ej: 'Sub-15')."""
        player_age = self.age

        if player_age <= 7:
            return "Sub-11"
        if player_age <= 9:
            return "Sub-9"
        if player_age <= 11:
            return "Sub-11"
        elif player_age <= 13:
            return "Sub-13"
        elif player_age <= 15:
            return "Sub-15"
        elif player_age <= 17:
            return "Sub-17"
        else:
            return "Primera"