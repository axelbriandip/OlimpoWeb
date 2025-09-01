from django.db import models

class Album(models.Model):
    title = models.CharField("Título del Álbum", max_length=200)
    description = models.TextField("Descripción (Opcional)", blank=True)
    created_on = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    
    class Meta:
        verbose_name = "Álbum"
        verbose_name_plural = "Álbumes"
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name="Álbum")
    title = models.CharField("Título (Opcional)", max_length=200, blank=True)
    image = models.ImageField("Imagen", upload_to='gallery/')
    uploaded_on = models.DateTimeField("Fecha de Subida", auto_now_add=True)

    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"
        ordering = ['-uploaded_on']

    def __str__(self):
        return self.title or f"Foto en {self.album.title}"