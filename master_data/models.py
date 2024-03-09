from django.db import models, transaction
from sequences import Sequence


# Create your models here.
def sequence_generated(name):
    return next(Sequence(sequence_name=name))


class DocumentType(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre",
    )
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipos de documento"


class Tax(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    percentage = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="Porcentaje"
    )
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Impuesto"
        verbose_name_plural = "Impuestos"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Metodo de pago"
        verbose_name_plural = "Metodos de pago"


class SaleType(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nombre")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Compañia"
        verbose_name_plural = "Compañias"


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
        self.name = self.name.upper()

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
