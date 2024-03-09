from django.contrib import admin
from .models import Payment

# Register your models here.


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
