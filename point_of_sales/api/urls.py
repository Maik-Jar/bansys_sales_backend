from django.urls import path, include
from .api import (
    InvoiceHeaderApiView,
    InvoiceHeaderListAPIView,
    CustomAuthToken,
    QuotationHeaderApiView,
)

urlpatterns = [
    path("api/login", CustomAuthToken.as_view()),
    path("api/invoices", InvoiceHeaderApiView.as_view(), name="invoices"),
    path("api/quotations", QuotationHeaderApiView.as_view(), name="quotations"),
    path("api/invoices_list", InvoiceHeaderListAPIView.as_view()),
    path("api/print/", include("point_of_sales.urls")),
]
