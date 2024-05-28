from django.db import models
from django.contrib.auth.models import User
from master_data.models import PaymentMethod
from point_of_sales.models import InvoiceHeader
from customers.models import Customer

# import locale

# Create your models here.
# locale.setlocale(locale.LC_MONETARY, "es_DO.UTF-8")


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto"
    )
    invoice = models.ForeignKey(
        InvoiceHeader,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="Pago",
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
    user_created = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name="payment_user_created",
        verbose_name="Creado por",
    )
    user_updated = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        editable=False,
        related_name="payment_user_updated",
        verbose_name="Modificado por",
    )
    inactive_comment = models.CharField(max_length=250, null=True, blank=True)

    def inactivate(self, comment, user):
        self.status = False
        self.user_updated = user
        self.inactive_comment = f"""Inactivado por: {user.first_name.upper()} {user.last_name.upper()} ({user.username}). \nMotivo: {comment}."""
        self.save()

        if self.invoice.status:
            if 0 < self.invoice.calculate_pending(1):
                self.invoice.pending_payment = True
                self.invoice.save()

    # def formatCurrencyPayment(self):
    #     return locale.currency(self.amount, grouping=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            if self.invoice.pending_payment:
                if self.amount >= self.invoice.calculate_pending(1):
                    self.invoice.pending_payment = False
                    self.invoice.save()
            else:
                raise ("Esta factura no esta pendiente de pago.")

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"


class Balance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
