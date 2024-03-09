from django.contrib import admin
from .models import (
    Output,
    Input,
    Return,
)


# Register your models here.


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
