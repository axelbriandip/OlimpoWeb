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