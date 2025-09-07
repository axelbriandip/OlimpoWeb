from django.db import models
from django.utils import timezone
from django.utils.text import slugify

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
    # Hacemos que el slug pueda estar en blanco, ya que lo generaremos nosotros
    slug = models.SlugField("Slug (URL)", max_length=200, unique=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    
    # --- Contenido ---
    featured_image = models.ImageField("Imagen Destacada", upload_to='news_images/', blank=True, null=True)
    excerpt = models.TextField("Extracto o Resumen", blank=True)
    content = models.TextField("Contenido")
    
    # --- Metadatos ---
    status = models.CharField("Estado", max_length=2, choices=Status.choices, default=Status.DRAFT)
    created_on = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    updated_on = models.DateTimeField("Última Actualización", auto_now=True)
    
     # 2. AÑADIMOS EL MÉTODO save
    def save(self, *args, **kwargs):
        # Si el slug está vacío, lo generamos a partir del título
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Nos aseguramos de que el slug sea único
        # Si ya existe un artículo con el mismo slug, le añadimos un número
        original_slug = self.slug
        counter = 1
        while Article.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{original_slug}-{counter}'
            counter += 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        return self.title