from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from functools import reduce
from sequences import Sequence, get_last_value
import locale

locale.setlocale(locale.LC_MONETARY, "es_DO")


def sequence_generated(name):
    return next(Sequence(sequence_name=name))


# Create your models here.


class DocumentType(models.Model):
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=30)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class SaleType(models.Model):
    name = models.CharField(max_length=60)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name="company_document_type"
    )
    document_id = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)
    logo = models.ImageField(upload_to="company/")

    def format_phone(self):
        return f"({self.phone[0:3]}) {self.phone[3:6]}-{self.phone[6:10]}"

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50)
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name="document_type"
    )
    document_id = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)

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


class Receipt(models.Model):
    name = models.CharField(max_length=25)
    serial = models.CharField(max_length=3, unique=True)
    init = models.IntegerField()
    end = models.IntegerField()
    expiration = models.DateField()
    status = models.BooleanField(default=True)

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


class SequenceReceipt(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=12)
    to_reuse = models.BooleanField(default=False, editable=False)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def mark_to_reuse(self):
        if self.receipt.expiration.year >= timezone.now().year:
            self.to_reuse = True
            self.save()

    def unmark_to_reuse(self):
        self.to_reuse = False
        self.save()

    def inactivate(self):
        self.to_reuse = False
        self.status = False
        self.save()

    def __str__(self) -> str:
        return f"{self.receipt.name} : {self.sequence}"

    def save(self, *args, **kwargs):
        if not self.sequence:
            if not (get_last_value(f"{self.receipt.serial}") >= self.receipt.end):
                self.sequence = str(sequence_generated(f"{self.receipt.serial}")).zfill(
                    8
                )
            else:
                raise Exception(
                    "No se puede generar secuencia del comprobante porque a alcanzado el limite."
                )

        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receipt", "sequence"], name="unique_sequence_receipt"
            )
        ]


class Provider(models.Model):
    name = models.CharField(max_length=50)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_id = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_id"],
                name="unique_provide_document_type_and_id",
            ),
        ]


class Item(models.Model):
    name = models.CharField(max_length=70)
    brand = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    is_service = models.BooleanField(default=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

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


class InvoiceHeader(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    number = models.CharField(max_length=12, unique=True, editable=False)
    receipt_type = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    sequence_receipt = models.ForeignKey(
        SequenceReceipt, on_delete=models.CASCADE, unique=True, null=True
    )
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sales_type = models.ForeignKey(SaleType, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user_created"
    )
    user_updated = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user_updated"
    )
    status = models.BooleanField(default=True, editable=False)

    def inactivate(self):
        self.status = False
        if self.sequence_receipt is not None:
            self.sequence_receipt.mark_to_reuse()
            self.sequence_receipt = None

        self.save()

    def calculateTotalQuantity(self):
        return reduce((lambda x, y: x + y.quantity), self.invoice_detail.all(), 0)

    def calculateTotalTax(self):
        return locale.currency(
            reduce((lambda x, y: x + y.calculateTax()), self.invoice_detail.all(), 0),
            grouping=True,
        )

    def calculateTotalDiscount(self):
        return locale.currency(
            reduce(
                (lambda x, y: x + y.calculateDiscount()), self.invoice_detail.all(), 0
            ),
            grouping=True,
        )

    def calculateTotalAmount(self):
        return locale.currency(
            reduce(
                (lambda x, y: x + y.calculateAmount()), self.invoice_detail.all(), 0
            ),
            grouping=True,
        )

    def __str__(self) -> str:
        return f"{self.id} / {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"{timezone.now().year}" + str(
                sequence_generated(f"invoice_number-{timezone.now().year}")
            ).zfill(5)

        return super().save(*args, **kwargs)


class InvoiceDetail(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, related_name="invoice_detail"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2)

    def inactivate(self):
        self.item.increase_stock(self.quantity)

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
        return f"{self.invoice_header.id} / {self.id} / {self.item.name}"

    def delete(self, *args, **kwargs):
        self.item.increase_stock(self.quantity)

        return super().delete(*args, **kwargs)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    invoice = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, related_name="payment"
    )
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def inactivate(self):
        self.status = False
        self.save()

    def formatCurrencyPayment(self):
        return locale.currency(self.amount, grouping=True)


class Output(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    reason = models.CharField(max_length=50)
    departure_date = models.DateTimeField(auto_now_add=True)

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


class Input(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    purchase_order = models.CharField(max_length=12)
    invoice_number = models.CharField(max_length=12)
    date_of_entry = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.item.name} / {self.date_of_entry}"

    def save(self, *args, **kwargs):
        if self.item.is_service:
            raise Exception("No se aumenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock + self.quantity
            self.item.save()

        return super().save(*args, **kwargs)


class Return(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    reason = models.CharField(max_length=50)
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.item.name} / {self.return_date}"

    def save(self, *args, **kwargs):
        if self.item.is_service:
            raise Exception("No se aumenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock + self.quantity
            self.item.save()

        return super().save(*args, **kwargs)
