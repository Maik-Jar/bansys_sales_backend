from django.urls import path
from .views import print_invoice, print_quotation, print_invoice_60mm

urlpatterns = [
    path("print_invoice", print_invoice),
    path("print_quotation", print_quotation),
    path("print_invoice_60mm", print_invoice_60mm),
]
