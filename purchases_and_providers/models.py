from django.db import models
from master_data.models import DocumentType

# Create your models here.


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

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_id"],
                name="unique_provide_document_type_and_id",
            ),
        ]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
