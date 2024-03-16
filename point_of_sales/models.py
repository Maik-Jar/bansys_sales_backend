from django.db import models
from django.contrib.auth.models import User
from master_data.models import SaleType, Receipt
from customers.models import Customer
from products_and_services.models import Item
from django.utils import timezone
from functools import reduce
from sequences import Sequence, get_last_value
import locale

locale.setlocale(locale.LC_MONETARY, "es_DO.UTF-8")


def sequence_generated(name):
    return next(Sequence(sequence_name=name))


# Create your models here.


class QuotationHeader(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quotation_customer",
        verbose_name="Cliente",
    )
    number = models.CharField(
        max_length=12, unique=True, editable=False, verbose_name="No. Cotización"
    )
    tax = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00, verbose_name="Impuesto"
    )
    discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Descuento"
    )
    sales_type = models.ForeignKey(
        SaleType, on_delete=models.CASCADE, verbose_name="Tipo de venta"
    )
    comment = models.CharField(
        max_length=400, null=True, blank=True, verbose_name="Comentarios"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )
    user_created = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="quotation_user_created",
        verbose_name="Creado por",
    )
    user_updated = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="quotation_user_updated",
        verbose_name="Actualizado por",
    )
    status = models.BooleanField(default=True, editable=False, verbose_name="Estado")

    def inactivate(self):
        self.status = False
        self.save()

    def calculate_subtotal(self, use=2):
        # 1: internal, 2: external
        if use == 1:
            return reduce(
                (lambda x, y: x + y.calculate_amount(1)), self.quotation_detail.all(), 0
            )
        else:
            return locale.currency(
                reduce(
                    (lambda x, y: x + y.calculate_amount(1)),
                    self.quotation_detail.all(),
                    0,
                ),
                grouping=True,
            )

    def calculate_total_quantity(self):
        return reduce((lambda x, y: x + y.quantity), self.quotation_detail.all(), 0)

    def calculate_total_discount(self, use=2):
        if use == 1:
            return (
                self.calculate_subtotal(1) * self.discount
                if 0 < self.discount < 1
                else self.discount
            )
        else:
            return locale.currency(
                (
                    self.calculate_subtotal(1) * self.discount
                    if self.discount < 1
                    else self.discount
                ),
                grouping=True,
            )

    def calculate_total_tax(self, use=2):
        if use == 1:
            return (self.calculate_subtotal(1) - self.calculate_total_discount(1)) * (
                self.tax
            )
        else:
            return locale.currency(
                (self.calculate_subtotal(1) - self.calculate_total_discount(1))
                * (self.tax),
                grouping=True,
            )

    def calculate_total_amount(self, use=2):
        if use == 1:
            return (
                self.calculate_subtotal(1) - self.calculate_total_discount(1)
            ) + self.calculate_total_tax(1)
        else:
            return locale.currency(
                (self.calculate_subtotal(1) - self.calculate_total_discount(1))
                + self.calculate_total_tax(1),
                grouping=True,
            )

    def __str__(self) -> str:
        return f"{self.id} / {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"{timezone.now().year}" + str(
                sequence_generated(f"quotation_number-{timezone.now().year}")
            ).zfill(5)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"


class QuotationDetail(models.Model):
    quotation_header = models.ForeignKey(
        QuotationHeader, on_delete=models.CASCADE, related_name="quotation_detail"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="quotation_item"
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    description = models.CharField(
        blank=True, null=True, max_length=4000, verbose_name="Descripcion"
    )

    def calculate_discount(self):
        if 0 < self.discount < 1:
            return (self.price * self.quantity) * self.discount
        return self.discount

    def calculate_amount(self, use=2):
        # 1: internal, 2: external
        if use == 1:
            return (self.price * self.quantity) - self.calculate_discount()
        else:
            return locale.currency(
                (self.price * self.quantity) - self.calculate_discount(), grouping=True
            )

    def format_price(self):
        return locale.currency(self.price, grouping=True)

    def __str__(self) -> str:
        return f"{self.quotation_header.id} / {self.id} / {self.item.name}"

    def delete(self, *args, **kwargs):
        self.item.increase_stock(self.quantity)

        return super().delete(*args, **kwargs)


class InvoiceHeader(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer",
        verbose_name="Cliente",
    )
    number = models.CharField(
        max_length=12, unique=True, editable=False, verbose_name="No. Factura"
    )
    tax = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00, verbose_name="Impuesto"
    )
    discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Descuento"
    )
    sales_type = models.ForeignKey(
        SaleType, on_delete=models.CASCADE, verbose_name="Tipo de venta"
    )
    comment = models.CharField(
        max_length=400, null=True, blank=True, verbose_name="Comentarios"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )
    user_created = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="user_created",
        verbose_name="Creado por",
    )
    user_updated = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="user_updated",
        verbose_name="Actualizado por",
    )
    status = models.BooleanField(default=True, editable=False, verbose_name="Estado")
    pending_payment = models.BooleanField(
        default=True, editable=False, verbose_name="pendiente de pago"
    )
    inactive_comment = models.CharField(max_length=200, null=True, blank=True)

    def inactivate(self, comment, user):
        self.status = False
        self.user_updated = user
        self.inactive_comment = f"""Inactivado por: {user.first_name.upper()} {user.last_name.upper()} ({user.username}). \nMotivo: {comment}"""
        if self.pending_payment:
            self.pending_payment = False
        self.save()

    def calculate_subtotal(self, use=2):
        # 1: internal, 2: external
        if use == 1:
            return reduce(
                (lambda x, y: x + y.calculate_amount(1)), self.invoice_detail.all(), 0
            )
        else:
            return locale.currency(
                reduce(
                    (lambda x, y: x + y.calculate_amount(1)),
                    self.invoice_detail.all(),
                    0,
                ),
                grouping=True,
            )

    def calculate_total_quantity(self):
        return reduce((lambda x, y: x + y.quantity), self.invoice_detail.all(), 0)

    def calculate_total_discount(self, use=2):
        if use == 1:
            return (
                self.calculate_subtotal(1) * self.discount
                if 0 < self.discount < 1
                else self.discount
            )
        else:
            return locale.currency(
                (
                    self.calculate_subtotal(1) * self.discount
                    if self.discount < 1
                    else self.discount
                ),
                grouping=True,
            )

    def calculate_total_tax(self, use=2):
        if use == 1:
            return (self.calculate_subtotal(1) - self.calculate_total_discount(1)) * (
                self.tax
            )
        else:
            return locale.currency(
                (self.calculate_subtotal(1) - self.calculate_total_discount(1))
                * (self.tax),
                grouping=True,
            )

    def calculate_total_amount(self, use=2):
        if use == 1:
            return (
                self.calculate_subtotal(1) - self.calculate_total_discount(1)
            ) + self.calculate_total_tax(1)
        else:
            return locale.currency(
                (self.calculate_subtotal(1) - self.calculate_total_discount(1))
                + self.calculate_total_tax(1),
                grouping=True,
            )

    def calculate_pending(self, use=2):
        # 1: internal, 2: external
        if use == 1:
            return (
                self.calculate_total_amount(1)
                - reduce(
                    (lambda x, y: x + y.amount), self.payment.filter(status=True), 0
                )
                if (
                    self.calculate_total_amount(1)
                    - reduce(
                        (lambda x, y: x + y.amount), self.payment.filter(status=True), 0
                    )
                )
                > 0
                else 0
            )
        else:
            return locale.currency(
                (
                    self.calculate_total_amount(1)
                    - reduce(
                        (lambda x, y: x + y.amount), self.payment.filter(status=True), 0
                    )
                    if (
                        self.calculate_total_amount(1)
                        - reduce(
                            (lambda x, y: x + y.amount),
                            self.payment.filter(status=True),
                            0,
                        )
                    )
                    > 0
                    else 0
                ),
                grouping=True,
            )

    def __str__(self) -> str:
        return f"{self.number} / {self.customer.name} / {self.calculate_total_amount()}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"{timezone.now().year}" + str(
                sequence_generated(f"invoice_number-{timezone.now().year}")
            ).zfill(5)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"


class InvoiceDetail(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, related_name="invoice_detail"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    description = models.CharField(
        blank=True, null=True, max_length=4000, verbose_name="Descripcion"
    )

    def inactivate(self):
        self.item.increase_stock(self.quantity)

    def calculate_discount(self):
        if 0 < self.discount < 1:
            return (self.price * self.quantity) * self.discount
        return self.discount

    def calculate_amount(self, use=2):
        # 1: internal, 2: external
        if use == 1:
            return (self.price * self.quantity) - self.calculate_discount()
        else:
            return locale.currency(
                (self.price * self.quantity) - self.calculate_discount(), grouping=True
            )

    def format_price(self):
        return locale.currency(self.price, grouping=True)

    def __str__(self) -> str:
        return f"{self.invoice_header.id} / {self.id} / {self.item.name}"

    def delete(self, *args, **kwargs):
        self.item.increase_stock(self.quantity)

        return super().delete(*args, **kwargs)


class SequenceReceipt(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="sequence",
        verbose_name="Comprobante",
    )
    invoice = models.OneToOneField(
        InvoiceHeader,
        on_delete=models.CASCADE,
        related_name="receipt_sequence",
        null=True,
        verbose_name="Factura",
    )
    sequence = models.CharField(max_length=12, verbose_name="Secuencia")
    to_reuse = models.BooleanField(default=False, editable=False, verbose_name="Reusar")
    status = models.BooleanField(default=True, verbose_name="Estado")
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    expiration = models.DateField(verbose_name="fecha de expiración")

    def mark_to_reuse(self):
        if self.receipt.id != 1:
            if self.receipt.expiration.year >= timezone.now().year:
                self.to_reuse = True
                self.invoice = None
                self.save()

    def unmark_to_reuse(self, invoive_instance):
        if self.receipt.id != 1:
            self.to_reuse = False
            self.invoice = invoive_instance
            self.save()

    def inactivate(self):
        if self.receipt.id != 1:
            self.to_reuse = False
            self.status = False
            self.invoice = None
            self.save()

    def __str__(self) -> str:
        return f"{self.receipt.name} : {self.sequence}"

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = self.receipt.expiration

        if not self.sequence:
            if not (get_last_value(f"{self.receipt.serial}") >= self.receipt.end):
                self.sequence = str(sequence_generated(f"{self.receipt.serial}")).zfill(
                    8
                )
            else:
                raise Exception(
                    "No se puede generar secuencia del comprobante porque a alcanzado el limite."
                )

        if self.invoice is not None and self.to_reuse:
            self.to_reuse = False

        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receipt", "sequence"], name="unique_sequence_receipt"
            )
        ]
        verbose_name = "Secuencia de comprobante"
        verbose_name_plural = "Secuencia de comprobantes"
