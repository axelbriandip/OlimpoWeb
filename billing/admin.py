from django.contrib import admin
from .models import BillableItem, Invoice, Payment

@admin.register(BillableItem)
class BillableItemAdmin(admin.ModelAdmin):
    """
    Admin para el catálogo de ítems que se pueden cobrar.
    """
    list_display = ('name', 'amount', 'is_bonifiable')
    search_fields = ('name',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin para las facturas asignadas a los socios.
    """
    list_display = ('profile', 'item', 'amount', 'status', 'due_date')
    list_filter = ('status', 'item', 'due_date')
    search_fields = ('profile__user__username', 'item__name')
    autocomplete_fields = ('profile',) # Facilita la búsqueda de perfiles
    list_editable = ('status',) # Permite cambiar el estado desde la lista

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin para ver los comprobantes de pago subidos.
    """
    list_display = ('invoice', 'uploaded_at')
    list_display_links = ('invoice',)
    autocomplete_fields = ('invoice',) # Facilita la búsqueda de facturas
