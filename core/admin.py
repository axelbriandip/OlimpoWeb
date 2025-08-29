from django.contrib import admin
from .models import BoardMember, TimelineEvent

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'group', 'display_order')
    list_filter = ('group',)
    list_editable = ('display_order',)

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'parent', 'exact_date')
    list_filter = ('year',)
    # Opcional: para organizar mejor el formulario de edición
    fieldsets = (
        (None, {
            'fields': ('title', 'year', 'exact_date', 'parent')
        }),
        ('Contenido', {
            'fields': ('description', 'image')
        }),
    )