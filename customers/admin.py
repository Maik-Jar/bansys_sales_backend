from django.contrib import admin
from .models import Customer

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "document_type", "document_id")
