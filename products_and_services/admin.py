from django.contrib import admin
from .models import Item


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ("name", "id", "brand", "provider", "price", "stock")
    list_display = ("name", "id", "brand", "price", "stock")
    readonly_fields = ("stock",)
