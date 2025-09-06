from django import forms
from .models import Payment

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