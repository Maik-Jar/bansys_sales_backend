from django.urls import path, include
from .api import (
    InvoiceHeaderApiView,
    CustomAuthToken,
    QuotationHeaderApiView,
)

urlpatterns = [
    path("api/login", CustomAuthToken.as_view()),
    path("api/invoices", InvoiceHeaderApiView.as_view(), name="invoices"),
    path("api/print/", include("point_of_sales.urls")),
    path("api/quotations", QuotationHeaderApiView.as_view(), name="quotations"),
]
