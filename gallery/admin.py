from django.contrib import admin
from .models import Album, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3 # Muestra 3 campos vacíos para subir fotos
    fields = ('image', 'title',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    inlines = [PhotoInline]