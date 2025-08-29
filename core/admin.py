from django.contrib import admin
from .models import BoardMember, TimelineEvent, Testimonial

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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'relation', 'is_featured')
    list_filter = ('is_featured',)
    list_editable = ('is_featured',)