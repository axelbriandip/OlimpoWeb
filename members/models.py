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

class Membership(models.Model):
    """
    Guarda el estado de la membresía y los pagos de un socio.
    """
    class Status(models.TextChoices):
        ACTIVO = 'ACT', 'Activo (Cuota al día)'
        ATRASADO = 'ATR', 'Atrasado'
        INACTIVO = 'INA', 'Inactivo'

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name="Perfil del Socio")
    status = models.CharField("Estado de la Cuota", max_length=3, choices=Status.choices, default=Status.ACTIVO)
    last_payment_date = models.DateField("Fecha del Último Pago", null=True, blank=True)
    next_due_date = models.DateField("Fecha del Próximo Vencimiento", null=True, blank=True)

    class Meta:
        verbose_name = "Estado de Membresía"
        verbose_name_plural = "Estados de Membresías"

    def __str__(self):
        return f"Membresía de {self.profile.user.username}"

class Payment(models.Model):
    """
    Guarda el registro de un pago individual realizado por un socio.
    """
    # Vinculamos el pago al perfil del socio
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="payments")
    
    # El archivo del comprobante
    receipt = models.ImageField("Comprobante de Pago", upload_to='receipts/')
    
    # Fecha en que el socio realizó el pago (la reporta él)
    payment_date = models.DateField("Fecha de Pago", auto_now_add=True)
    
    # Fecha en que se subió el comprobante
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago Registrado"
        verbose_name_plural = "Pagos Registrados"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Pago de {self.profile.user.username} el {self.payment_date}"