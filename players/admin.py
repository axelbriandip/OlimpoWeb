from django.contrib import admin
from .models import Player, Category

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('first_name', 'last_name', 'dni')
    # 'filter_horizontal' es ideal para campos ManyToManyField
    filter_horizontal = ('managed_categories',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)