from django.contrib import admin
from .models import Article, NewsCategory

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """
    Configuración del Admin para las Categorías de Noticias.
    """
    list_display = ('name',)
    # Esto hace que el campo 'slug' se rellene automáticamente al escribir el nombre.
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Configuración del Admin para los Artículos (Noticias).
    """
    list_display = ('title', 'status', 'category', 'created_on')
    list_filter = ('status', 'category', 'created_on')
    search_fields = ('title', 'content')
    # Rellena automáticamente el slug a partir del título. ¡Muy útil!
    prepopulated_fields = {'slug': ('title',)}