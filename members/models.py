from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Este modelo extiende el modelo User de Django para añadir campos adicionales.
    """
    # Relación uno a uno: cada Usuario tiene un solo Perfil.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos adicionales del socio
    dni = models.CharField("DNI", max_length=20, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)
    phone_number = models.CharField("Teléfono", max_length=50, blank=True)
    # Aquí puedes añadir más campos en el futuro, como 'fecha de inscripción', etc.

    def __str__(self):
        return f'Perfil de {self.user.username}'