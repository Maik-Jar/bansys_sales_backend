from django.db import models
from master_data.models import DocumentType

# Create your models here.


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

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_id"],
                name="unique_customer_document_id_and_document_type",
                condition=models.Q(document_id__isnull=False),
            ),
        ]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
