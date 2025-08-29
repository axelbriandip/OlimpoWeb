from django.contrib import admin
from .models import BoardMember

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'group', 'display_order')
    list_filter = ('group',)
    list_editable = ('display_order',)