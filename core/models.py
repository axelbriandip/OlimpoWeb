from django.db import models

class BoardMember(models.Model):
    # Definimos las opciones para los grupos
    class MemberGroup(models.TextChoices):
        MESA_DIRECTIVA = 'Mesa Directiva', 'Mesa Directiva'
        VOCALES = 'Vocales', 'Vocales'
        FISCALIZADORES = 'Comisión Fiscalizadora', 'Comisión Fiscalizadora'

    full_name = models.CharField("Nombre Completo", max_length=200)
    role = models.CharField("Cargo", max_length=100)
    photo = models.ImageField("Foto", upload_to='board_members/', blank=True, null=True)
    display_order = models.PositiveIntegerField("Orden", default=0, help_text="Menor número aparece primero")
    
    # --- CAMPO NUEVO PARA EL GRUPO ---
    group = models.CharField(
        "Grupo",
        max_length=50,
        choices=MemberGroup.choices,
        default=MemberGroup.MESA_DIRECTIVA
    )

    class Meta:
        verbose_name = "Miembro de la Directiva"
        verbose_name_plural = "Miembros de la Directiva"
        # Ordenamos primero por grupo y luego por el orden manual
        ordering = ['group', 'display_order']

    def __str__(self):
        return self.full_name

class TimelineEvent(models.Model):
    """Representa un único evento en la línea de tiempo de la historia del club."""
    
    year = models.PositiveIntegerField("Año")
    title = models.CharField("Título del Hito", max_length=200)
    description = models.TextField("Descripción")
    image = models.ImageField("Imagen", upload_to='history_images/', blank=True, null=True)
    exact_date = models.DateField("Fecha Exacta (Opcional)", null=True, blank=True)
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='sub_events',
        verbose_name="Hito Padre (si es un sub-hito)"
    )

    class Meta:
        verbose_name = "Hito de la Historia"
        verbose_name_plural = "Hitos de la Historia"
        ordering = ['year']

    def __str__(self):
        return f"{self.year} - {self.title}"

class Testimonial(models.Model):
    """Representa un testimonio de un miembro, padre o jugador."""
    quote = models.TextField("Cita o Testimonio")
    author = models.CharField("Autor", max_length=100)
    relation = models.CharField("Relación con el Club", max_length=100, 
                                help_text="Ej: Padre de jugador Sub-15, Socio Fundador, Jugadora de Primera")
    photo = models.ImageField("Foto (Opcional)", upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(
        "Destacar en Inicio", 
        default=False,
        help_text="Marcar para que este testimonio pueda aparecer en la página de inicio."
    )
    
    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ['author']

    def __str__(self):
        return f'Testimonio de {self.author}'