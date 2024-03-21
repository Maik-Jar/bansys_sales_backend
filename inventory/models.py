from django.db import models
from products_and_services.models import Item
from purchases_and_providers.models import Provider

# Create your models here.


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
        self.reason = self.reason.upper()

        if self.item.stock < 1 or self.quantity > self.item.stock:
            raise Exception("La cantidad que intenta descontar es mayor que el stock.")
        if self.item.is_service:
            raise Exception("No se descuenta de stock cuando es un servicio.")
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
    purchase_order = models.CharField(
        blank=True, null=True, max_length=12, verbose_name="Orden de compra"
    )
    invoice_number = models.CharField(
        blank=True, null=True, max_length=12, verbose_name="No. Factura"
    )
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
        self.reason = self.reason.upper()

        if self.item.is_service:
            raise Exception("No se aumenta de stock cuando es un servicio.")
        else:
            self.item.stock = self.item.stock + self.quantity
            self.item.save()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Devolución"
        verbose_name_plural = "Devoluciones"
