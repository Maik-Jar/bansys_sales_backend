from django.contrib import admin
from .models import Provider


# Register your models here.
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_filter = ("name", "document_type", "document_id")
    list_display = ("name", "document_type", "document_id")
