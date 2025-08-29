from django.db import models

class BoardMember(models.Model):
    # Representa a un miembro de la Comisión Directiva.
    full_name = models.CharField("Nombre Completo", max_length=200)
    role = models.CharField("Cargo", max_length=100)
    photo = models.ImageField("Foto", upload_to='board_members/', blank=True, null=True)
    display_order = models.PositiveIntegerField("Orden", default=0, help_text="Menor número aparece primero")

    class Meta:
        verbose_name = "Miembro de la Directiva"
        verbose_name_plural = "Miembros de la Directiva"
        ordering = ['display_order']

    def __str__(self):
        return self.full_name