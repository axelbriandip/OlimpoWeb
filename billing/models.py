# billing/models.py

from django.db import models

class BillableItem(models.Model):
    name = models.CharField("Nombre del Ítem", max_length=200)
    amount = models.DecimalField("Monto", max_digits=10, decimal_places=2)
    is_bonifiable = models.BooleanField("Es Bonificable", default=True)

    class Meta:
        verbose_name = "Ítem Facturable"
        verbose_name_plural = "Ítems Facturables"
    def __str__(self):
        return f"{self.name} - ${self.amount}"

class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDIENTE = 'PEN', 'Pendiente de Pago'
        EN_VERIFICACION = 'VER', 'En Verificación'
        PAGADO = 'PAG', 'Pagado'
        BONIFICADO = 'BON', 'Bonificado'

    profile = models.ForeignKey('members.Profile', on_delete=models.CASCADE, related_name="invoices")
    item = models.ForeignKey(BillableItem, on_delete=models.PROTECT, verbose_name="Ítem")
    amount = models.DecimalField("Monto", max_digits=10, decimal_places=2)
    status = models.CharField("Estado", max_length=3, choices=Status.choices, default=Status.PENDIENTE)
    due_date = models.DateField("Fecha de Vencimiento", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
    def __str__(self):
        return f"Factura para {self.profile.user.username} de {self.item.name}"

class Payment(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name="payment")
    receipt = models.ImageField("Comprobante de Pago", upload_to='receipts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comprobante para la factura #{self.invoice.id}"