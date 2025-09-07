from django import forms
from .models import Payment, BillableItem

class ReceiptUploadForm(forms.ModelForm):
    """
    Formulario para que el socio suba su comprobante de pago.
    """
    class Meta:
        model = Payment
        fields = ['receipt']
        labels = {
            'receipt': 'Adjuntar comprobante (captura o foto)',
        }

class BillableItemForm(forms.ModelForm):
    """
    Formulario para crear y editar Ítems Facturables.
    """
    class Meta:
        model = BillableItem
        fields = ['name', 'amount', 'is_bonifiable']
        labels = {
            'name': 'Nombre del Ítem (ej: Cuota Octubre, Inscripción 2025)',
            'amount': 'Monto a Cobrar',
            'is_bonifiable': '¿Este ítem puede ser bonificado?',
        }