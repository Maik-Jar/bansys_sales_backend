from django.db import models
from purchases_and_providers.models import Provider

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nombre")
    brand = models.CharField(max_length=20, blank=True, null=True, verbose_name="Marca")
    reference = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Referencia"
    )
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, verbose_name="Precio"
    )
    discount = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, verbose_name="Descuento"
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

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

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
