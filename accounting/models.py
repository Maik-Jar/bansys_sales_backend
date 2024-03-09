from django.db import models
from master_data.models import PaymentMethod
from point_of_sales.models import InvoiceHeader
from customers.models import Customer
import locale

# Create your models here.
locale.setlocale(locale.LC_MONETARY, "es_DO.UTF-8")


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto"
    )
    invoice = models.ForeignKey(
        InvoiceHeader,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="Factura",
    )
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, verbose_name="Método de pago"
    )
    status = models.BooleanField(default=True, verbose_name="Estado")
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    def inactivate(self):
        self.status = False
        self.save()

    def formatCurrencyPayment(self):
        return locale.currency(self.amount, grouping=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"


class Balance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
