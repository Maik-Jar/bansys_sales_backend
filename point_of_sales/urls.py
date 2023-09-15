from django.urls import path
from .views import print_invoice, print_quotation

urlpatterns = [
    path("print_invoice", print_invoice),
    path("print_quotation", print_quotation),
]
