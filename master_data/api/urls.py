from django.urls import path
from .api import (
    DocumentTypeAPIView,
    TaxListAPIView,
    ReceiptListAPIView,
    SalesTypeListAPIView,
    PaymentMethodListAPIView,
)

urlpatterns = [
    path("api/receipts", ReceiptListAPIView.as_view()),
    path("api/documents_types", DocumentTypeAPIView.as_view()),
    path("api/taxes", TaxListAPIView.as_view()),
    path("api/sales_types", SalesTypeListAPIView.as_view(), name="sales_types"),
    path(
        "api/payments_methods",
        PaymentMethodListAPIView.as_view(),
        name="payments_methods",
    ),
]
