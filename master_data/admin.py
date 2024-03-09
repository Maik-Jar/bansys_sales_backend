from django.contrib import admin
from .models import (
    DocumentType,
    Tax,
    PaymentMethod,
    SaleType,
    Receipt,
    Company,
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


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_filter = ("name", "serial", "expiration")
    list_display = ("name", "id", "serial", "expiration")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "document_type", "document_id")
