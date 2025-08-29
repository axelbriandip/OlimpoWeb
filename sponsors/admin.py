from django.contrib import admin
from .models import Sponsor

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'website_url')
    list_editable = ('display_order',)
    search_fields = ('name',)