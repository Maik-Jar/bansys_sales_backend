from django.urls import path, include
from .api import (
    InvoiceHeaderApiView,
    InvoiceHeaderListAPIView,
    InvoicePrintListAPIView,
    CustomAuthToken,
    QuotationHeaderApiView,
    QuotationPrintListAPIView,
)

urlpatterns = [
    path("api/login", CustomAuthToken.as_view()),
    path("api/invoices", InvoiceHeaderApiView.as_view(), name="invoices"),
    path("api/quotations", QuotationHeaderApiView.as_view(), name="quotations"),
    path("api/invoices_list", InvoiceHeaderListAPIView.as_view()),
    path("api/invoice_print_data", InvoicePrintListAPIView.as_view()),
    path("api/quotation_print_data", QuotationPrintListAPIView.as_view()),
    # path("api/print/", include("point_of_sales.urls")),
]
