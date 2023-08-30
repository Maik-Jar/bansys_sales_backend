from django.db import models
from django.contrib.auth.models import User


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


class Customer(models.Model):
    name = models.CharField(max_length=50)
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name="document_type"
    )
    document_id = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=70, blank=True, null=True)

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


class SequenceReceipt(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    sequence = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.receipt.name} : {self.sequence}"

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
    number = models.CharField(max_length=12, unique=True)
    receipt_type = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    sequence_receipt = models.ForeignKey(
        SequenceReceipt, on_delete=models.CASCADE, unique=True, null=True
    )
    # subtotal = models.DecimalField(max_digits=12, decimal_places=2)# TODO: debe morir
    # total_tax = models.DecimalField(max_digits=12, decimal_places=2)# TODO: debe morir
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # total = models.DecimalField(max_digits=12, decimal_places=2) # TODO: debe morir
    # Payment = models.ManyToManyField(Payment, default=0.00)
    # payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
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
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.id} / {self.customer.name}"


class InvoiceDetail(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, related_name="invoice_detail"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.invoice_header.id} / {self.id} / {self.item.name}"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    invoice = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, related_name="payment"
    )
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


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
