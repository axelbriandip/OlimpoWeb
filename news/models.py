from django.db import models
from django.utils import timezone

class NewsCategory(models.Model):
    """Representa una categoría para una noticia (ej: 'Resultados', 'Eventos')."""
    name = models.CharField("Nombre", max_length=100, unique=True)
    slug = models.SlugField("Slug (URL)", max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría de Noticia"
        verbose_name_plural = "Categorías de Noticias"
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    """Representa un artículo o una noticia del club."""

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Borrador'
        PUBLISHED = 'PB', 'Publicado'

    # --- Atributos Principales ---
    title = models.CharField("Título", max_length=200)
    subtitle = models.CharField("Subtítulo", max_length=200, blank=True)
    slug = models.SlugField("Slug (URL)", max_length=200, unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    
    # --- Contenido ---
    featured_image = models.ImageField("Imagen Destacada", upload_to='news_images/', blank=True, null=True)
    excerpt = models.TextField("Extracto o Resumen", blank=True)
    content = models.TextField("Contenido")
    
    # --- Metadatos ---
    status = models.CharField("Estado", max_length=2, choices=Status.choices, default=Status.DRAFT)
    created_on = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    updated_on = models.DateTimeField("Última Actualización", auto_now=True)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        return self.title