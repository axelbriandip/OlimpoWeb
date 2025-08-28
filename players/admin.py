from django.contrib import admin
from .models import Player, Category # Importar Category

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('first_name', 'last_name', 'dni')
    # 'filter_horizontal' es ideal para campos ManyToManyField
    filter_horizontal = ('managed_categories',)

# Registrar el nuevo modelo
admin.site.register(Category)