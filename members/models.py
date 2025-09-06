# members/models.py
from django.db import models
from django.contrib.auth.models import User

class SpecificPosition(models.Model):
    """Cargos específicos que se pueden asignar (ej: Delantero, Tesorero)."""
    name = models.CharField("Nombre del Cargo", max_length=100, unique=True)

    class Meta:
        verbose_name = "Cargo Específico"
        verbose_name_plural = "Cargos Específicos"
        ordering = ['name']

    def __str__(self):
        return self.name

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

class MemberType(models.Model):
    """ Tipos de Socio (ej: Jugador, Adherente), gestionable desde el admin. """
    name = models.CharField("Nombre del Tipo de Socio", max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Tipo de Socio"
        verbose_name_plural = "Tipos de Socio"
        ordering = ['name']

    def __str__(self):
        return self.name

class Role(models.Model):
    """ Un rol específico que una persona puede tener (ej: Delantero en Primera). """
    class Function(models.TextChoices):
        JUGADOR = 'JUG', 'Jugador'
        STAFF = 'STA', 'Cuerpo Técnico'
        DIRIGENTE = 'DIR', 'Dirigente'

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='roles')
    function = models.CharField("Función", max_length=3, choices=Function.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría (si aplica)")
    specific_position = models.CharField("Cargo Específico", max_length=100, help_text="Ej: Delantero, Tesorero, Director Técnico")
    
    specific_position = models.ForeignKey(
        SpecificPosition, 
        on_delete=models.PROTECT,
        verbose_name="Cargo Específico"
    )

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return f"{self.profile.user.username} - {self.get_function_display()}: {self.specific_position}"

# 1. FUNCIÓN PARA EL NÚMERO DE SOCIO AUTOMÁTICO
def get_next_member_id():
    """
    Busca el número de socio más alto y devuelve el siguiente.
    Si no hay socios, empieza en 1.
    """
    last_profile = Profile.objects.order_by('-member_id').first()
    if last_profile and last_profile.member_id:
        return last_profile.member_id + 1
    return 1

class Profile(models.Model):
    """ El Perfil Único que centraliza toda la información de una persona. """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# 1. NÚMERO DE SOCIO AUTOMÁTICO
    member_id = models.PositiveIntegerField(
        "Número de Socio", 
        unique=True, 
        default=get_next_member_id, 
        editable=False # Hacemos que no se pueda editar desde el admin
    )
    date_of_birth = models.DateField("Fecha de Nacimiento", null=True, blank=True)
    dni = models.CharField("DNI", max_length=20, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)
    phone_number = models.CharField("Teléfono", max_length=50, blank=True)
    
    profile_photo = models.ImageField("Foto de Perfil", upload_to='profile_photos/', blank=True, null=True)
    extra_photo_1 = models.ImageField("Foto Extra 1 (opcional)", upload_to='extra_photos/', blank=True, null=True)
    extra_photo_2 = models.ImageField("Foto Extra 2 (opcional)", upload_to='extra_photos/', blank=True, null=True)
    dni_photo_front = models.ImageField("Foto DNI (Frente)", upload_to='dni_photos/', blank=True, null=True)
    dni_photo_back = models.ImageField("Foto DNI (Dorso)", upload_to='dni_photos/', blank=True, null=True)
    
    member_type = models.ForeignKey(MemberType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Socio")
    is_on_roster = models.BooleanField("En Lista Oficial (para jugadores)", default=False)
    is_exempt = models.BooleanField("Cuota Bonificada", default=False)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'