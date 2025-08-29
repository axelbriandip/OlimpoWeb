from django.db import models

class Sponsor(models.Model):
    name = models.CharField("Nombre del Sponsor", max_length=100)
    logo = models.ImageField("Logo", upload_to='sponsors/')
    website_url = models.URLField("URL del Sitio Web (Opcional)", blank=True, null=True)
    display_order = models.PositiveIntegerField("Orden de Visualización", default=0, 
                                                help_text="Menor número aparece primero")

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name