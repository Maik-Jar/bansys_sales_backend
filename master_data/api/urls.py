from django.urls import path
from .api import (
    DocumentTypeAPIView,
    DocumentTypeListAPIView,
    TaxAPIView,
    TaxListAPIView,
    ReceiptAPIView,
    ReceiptListAPIView,
    SalesTypeAPIView,
    SalesTypeListAPIView,
    PaymentMethodAPIView,
    PaymentMethodListAPIView,
    CompanyListAPIView,
)

urlpatterns = [
    path("api/receipts", ReceiptAPIView.as_view()),
    path("api/receipts_list", ReceiptListAPIView.as_view()),
    path("api/documents_types", DocumentTypeAPIView.as_view()),
    path("api/documents_types_list", DocumentTypeListAPIView.as_view()),
    path("api/taxes", TaxAPIView.as_view()),
    path("api/taxes_list", TaxListAPIView.as_view()),
    path("api/sales_types", SalesTypeAPIView.as_view()),
    path("api/sales_types_list", SalesTypeListAPIView.as_view()),
    path(
        "api/payments_methods",
        PaymentMethodAPIView.as_view(),
    ),
    path(
        "api/payments_methods_list",
        PaymentMethodListAPIView.as_view(),
    ),
    path(
        "api/company_list",
        CompanyListAPIView.as_view(),
    ),
]
