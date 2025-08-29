from django.contrib import admin
from .models import BoardMember

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    # Configuración del Admin para los Miembros de la Directiva.
    list_display = ('full_name', 'role', 'display_order')
    list_editable = ('display_order',)