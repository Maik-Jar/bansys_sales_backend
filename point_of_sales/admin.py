from django.contrib import admin
from .models import (
    DocumentType,
    Tax,
    PaymentMethod,
    SaleType,
    Customer,
    Receipt,
    Provider,
    Item,
    Output,
    Input,
    Return,
    SequenceReceipt,
    Payment,
    Company,
    QuotationHeader,
    InvoiceHeader,
)


# Register your models here.
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_filter = ("id", "name")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_filter = ("name", "percentage")
    list_display = ("name", "percentage")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_filter = ("name",)


@admin.register(SaleType)
class SaleTypeAdmin(admin.ModelAdmin):
    list_filter = ("name",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "document_type", "document_id")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_filter = ("name", "serial", "expiration")
    list_display = ("name", "id", "serial", "expiration")


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_filter = ("name", "document_type", "document_id")
    list_display = ("name", "document_type", "document_id")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ("name", "id", "brand", "provider", "price", "stock")
    list_display = ("name", "id", "brand", "price", "stock")
    readonly_fields = ("stock",)


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_filter = ("item", "quantity", "reason", "departure_date")
    list_display = ("item", "quantity", "reason", "departure_date")


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_filter = ("item", "quantity", "provider", "date_of_entry")
    list_display = ("item", "quantity", "provider", "date_of_entry")


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_filter = ("item", "quantity", "reason", "return_date")
    list_display = ("item", "quantity", "reason", "return_date")


@admin.register(SequenceReceipt)
class SequenceReceiptAdmin(admin.ModelAdmin):
    list_filter = ("receipt", "sequence", "to_reuse", "status")
    list_display = ("receipt", "sequence", "to_reuse", "status")
    readonly_fields = ("sequence", "receipt")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_filter = (
        "invoice",
        "amount",
        "payment_method",
        "status",
        "date_created",
        "date_updated",
    )
    list_display = ("invoice", "amount", "payment_method", "status")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "document_type", "document_id")


@admin.register(InvoiceHeader)
class InvoiceHeaderAdmin(admin.ModelAdmin):
    list_filter = ("customer", "number", "user_created", "user_updated")
    list_display = (
        "number",
        "customer",
        "receipt_sequence",
        "calculate_total_amount",
        "status",
    )


# @admin.register(QuotationHeader)
# class QuotationHeaderAdmin(admin.ModelAdmin):
#     list_filter = ("name",)
#     list_display = ("name", "document_type", "document_id")
