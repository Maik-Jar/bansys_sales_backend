from django.contrib import admin
from .models import (
    SequenceReceipt,
    QuotationHeader,
    InvoiceHeader,
)


# Register your models here.


@admin.register(SequenceReceipt)
class SequenceReceiptAdmin(admin.ModelAdmin):
    list_filter = ("receipt", "sequence", "to_reuse", "status")
    list_display = ("receipt", "sequence", "to_reuse", "status")
    readonly_fields = ("sequence", "receipt")


@admin.register(InvoiceHeader)
class InvoiceHeaderAdmin(admin.ModelAdmin):
    list_filter = ("customer", "number", "user_created", "user_updated")
    list_display = (
        "number",
        "customer",
        "receipt_sequence",
        "status",
    )


# @admin.register(QuotationHeader)
# class QuotationHeaderAdmin(admin.ModelAdmin):
#     list_filter = ("name",)
#     list_display = ("name", "document_type", "document_id")
