from django.db import models
from django.utils import timezone

class Player(models.Model):
    """Representa a un único jugador del club."""
    
    # --- Atributos Esenciales ---
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)
    photo = models.ImageField("Foto", upload_to='players/', blank=True, null=True)
    date_of_birth = models.DateField("Fecha de Nacimiento")
    birth_city = models.CharField("Ciudad de Nacimiento", max_length=100, blank=True)
    birth_province = models.CharField("Provincia de Nacimiento", max_length=100, blank=True)
    
    # --- Atributos Deportivos ---
    position = models.CharField("Posición", max_length=50, blank=True)
    bio = models.TextField("Biografía", blank=True)
    join_date = models.DateField("Fecha de Ingreso", default=timezone.now)

    # --- Atributos Administrativos (Privados) ---
    dni = models.CharField("DNI", max_length=20, blank=True)
    member_id = models.CharField("Número de Socio", max_length=50, blank=True)
    is_active = models.BooleanField("Está Activo", default=True) # Para borrados suaves

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Calcula la edad actual del jugador."""
        today = timezone.now().date()
        # Lógica para calcular la edad exacta teniendo en cuenta el día y mes
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))