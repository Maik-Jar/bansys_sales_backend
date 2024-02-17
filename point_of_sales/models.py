from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from functools import reduce
from sequences import Sequence, get_last_value
import locale

locale.setlocale(locale.LC_MONETARY, "es_DO.UTF-8")


def sequence_generated(name):
    return next(Sequence(sequence_name=name))


# Create your models here.


class DocumentType(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documento"


class Tax(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Porcentaje"
    )
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Impuesto"
        verbose_name_plural = "Impuestos"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Metodo de pago"
        verbose_name_plural = "Metodos de pago"


class SaleType(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nombre")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Tipo de venta"
        verbose_name_plural = "Tipos de venta"


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="company_document_type",
        verbose_name="Tipo de documento",
    )
    document_id = models.CharField(
        max_length=15, null=True, verbose_name="No. Documento"
    )
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    address = models.CharField(
        max_length=70, blank=True, null=True, verbose_name="Dirección"
    )
    logo = models.ImageField(upload_to="company/")

    def format_phone(self):
        return f"({self.phone[0:3]}) {self.phone[3:6]}-{self.phone[6:10]}"

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Compañia"
        verbose_name_plural = "Compañias"


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre completo")
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="document_type",
        verbose_name="Tido de documento",
    )
    document_id = models.CharField(
        max_length=15, null=True, verbose_name="No. Documento"
    )
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    address = models.CharField(
        max_length=70, blank=True, null=True, verbose_name="Dirección"
    )

    def format_phone(self):
        return f"({self.phone[0:3]}) {self.phone[3:6]}-{self.phone[6:10]}"

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_id"],
                name="unique_customer_document_type_and_id",
                condition=models.Q(document_id__isnull=False),
            ),
        ]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Receipt(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nombre")
    serial = models.CharField(max_length=3, unique=True)
    init = models.IntegerField(verbose_name="Inicio secuencia")
    end = models.IntegerField(verbose_name="Fin secuencia")
    expiration = models.DateField(verbose_name="Fecha de expiración")
    status = models.BooleanField(default=True, verbose_name="Estado")
    tax = models.ForeignKey(
        Tax, default=1, on_delete=models.CASCADE, verbose_name="Impuesto"
    )

    def __str__(self) -> str:
        return f"{self.name} : {self.serial}"

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                with transaction.atomic():
                    Sequence(
                        sequence_name=f"{self.serial}", initial_value=self.init - 1
                    ).get_next_value()
                    return super().save(*args, **kwargs)
            except:
                raise Exception(
                    "No se ha podido crear el comprobante por problemas internos."
                )

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Comprobante"
        verbose_name_plural = "Comprobantes"


class Provider(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, verbose_name="Tipo de documento"
    )
    document_id = models.CharField(max_length=15, verbose_name="No. Documento")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    address = models.CharField(
        max_length=70, blank=True, null=True, verbose_name="Dirección"
    )
    status = models.BooleanField(default=True, verbose_name="Estatus")

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_id"],
                name="unique_provide_document_type_and_id",
            ),
        ]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Item(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nombre")
    brand = models.CharField(max_length=20, blank=True, null=True, verbose_name="Marca")
    reference = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Referencia"
    )
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, verbose_name="Precio"
    )
    stock = models.IntegerField(default=0)
    stock_min = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Minimo"
    )
    stock_max = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Maximo"
    )
    is_service = models.BooleanField(default=False, verbose_name="Servicio?")
    provider = models.ManyToManyField(Provider, verbose_name="Proveedor")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    def increase_stock(self, quantity):
        if not self.is_service:
            self.stock = self.stock + quantity
            self.save()

    def decrease_stock(self, quantity):
        if not self.is_service:
            if self.stock < 1 or quantity > self.stock:
                raise Exception(
                    "La cantidad que intenta descontar es mayor que el stock."
                )

            self.stock = self.stock - quantity
            self.save()

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"


class QuotationHeader(models.Model):
    customer = models.JSONField(null=True, verbose_name="Cliente")
    number = models.CharField(
        max_length=12, unique=True, editable=False, verbose_name="No. Cotización"
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

    def calculateTotalQuantity(self):
        return reduce((lambda x, y: x + y.quantity), self.quotation_detail.all(), 0)

    def calculateTotalTax(self):
        return locale.currency(
            reduce((lambda x, y: x + y.calculateTax()), self.quotation_detail.all(), 0),
            grouping=True,
        )

    def calculateTotalDiscount(self):
        return locale.currency(
            reduce(
                (lambda x, y: x + y.calculateDiscount()), self.quotation_detail.all(), 0
            ),
            grouping=True,
        )

    def calculateTotalAmount(self):
        return locale.currency(
            reduce(
                (lambda x, y: x + y.calculateAmount()), self.quotation_detail.all(), 0
            ),
            grouping=True,
        )

    def __str__(self) -> str:
        return f"{self.id} / {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"{timezone.now().year}" + str(
                sequence_generated(f"quotation_number-{timezone.now().year}")
            ).zfill(5)

        if self.customer is not None:
            self.customer["name"] = self.customer["name"].upper()

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
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2)

    def calculateDiscount(self):
        if 0 < self.discount < 1:
            return (self.price * self.quantity) * self.discount
        return self.discount

    def calculateTax(self):
        return ((self.price * self.quantity) - self.calculateDiscount()) * self.tax

    def calculateAmount(self):
        return self.calculateTax() + (
            self.price * self.quantity - self.calculateDiscount()
        )

    def __str__(self) -> str:
        return f"{self.quotation_header.id} / {self.id} / {self.item.name}"


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
    avance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="abono"
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

    def inactivate(self):
        self.status = False

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
                self.calculate_total_amount()
                - reduce((lambda x, y: x + y.amount), self.payment.all(), 0)
                if (
                    self.calculate_total_amount()
                    - reduce((lambda x, y: x + y.amount), self.payment.all(), 0)
                )
                > 0
                else 0
            )
        else:
            return locale.currency(
                (
                    self.calculate_total_amount(1)
                    - reduce((lambda x, y: x + y.amount), self.payment.all(), 0)
                    if (
                        self.calculate_total_amount(1)
                        - reduce((lambda x, y: x + y.amount), self.payment.all(), 0)
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
    # tax = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def inactivate(self):
        self.item.increase_stock(self.quantity)

    def calculate_discount(self):
        if 0 < self.discount < 1:
            return (self.price * self.quantity) * self.discount
        return self.discount

    # def calculateTax(self):
    #     return ((self.price * self.quantity) - self.calculateDiscount()) * self.tax

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


class Output(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Artículo")
    quantity = models.IntegerField(default=1, verbose_name="Cantidad")
    reason = models.CharField(max_length=50, verbose_name="Razón")
    departure_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de salida"
    )

    def __str__(self) -> str:
        return f"{self.item.name} / {self.departure_date}"

    def save(self, *args, **kwargs):
        if self.item.stock < 1 or self.quantity > self.item.stock:
            raise Exception("La cantidad que intenta descontar es mayor que el stock.")
        if self.item.is_service:
            raise Exception("No se decuenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock - self.quantity
            self.item.save()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"


class Input(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Artículo")
    quantity = models.IntegerField(default=1, verbose_name="Cantidad")
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Proveedor"
    )
    purchase_order = models.CharField(max_length=12, verbose_name="Orden de compra")
    invoice_number = models.CharField(max_length=12, verbose_name="No. Factura")
    date_of_entry = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de entrada"
    )

    def __str__(self) -> str:
        return f"{self.item.name} / {self.date_of_entry}"

    def save(self, *args, **kwargs):
        if self.item.is_service:
            raise Exception("No se aumenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock + self.quantity
            self.item.save()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"


class Return(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Artículo")
    quantity = models.IntegerField(default=1, verbose_name="Cantidad")
    reason = models.CharField(max_length=50, verbose_name="Razón")
    return_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de devolución"
    )

    def __str__(self) -> str:
        return f"{self.item.name} / {self.return_date}"

    def save(self, *args, **kwargs):
        if self.item.is_service:
            raise Exception("No se aumenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock + self.quantity
            self.item.save()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Devolución"
        verbose_name_plural = "Devoluciones"
