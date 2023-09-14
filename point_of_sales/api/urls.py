from django.urls import path, include
from rest_framework.authtoken import views
from .api import (
    CustomerApiView,
    ProviderApiView,
    ItemApiView,
    InvoiceHeaderApiView,
    DocumentTypeAPIView,
    TaxListAPIView,
    ReceiptListAPIView,
    ItemListAPIView,
    SalesTypeListAPIView,
    PaymentMethodListAPIView,
    CustomAuthToken,
    # LoginAPIView,
    # LogoutAPIView,
)

urlpatterns = [
    path("api/login", CustomAuthToken.as_view()),
    path("api/receipts", ReceiptListAPIView.as_view()),
    path("api/documents_types", DocumentTypeAPIView.as_view()),
    path("api/taxes", TaxListAPIView.as_view()),
    path("api/customers", CustomerApiView.as_view(), name="customers"),
    path("api/providers", ProviderApiView.as_view(), name="providers"),
    path("api/items", ItemApiView.as_view(), name="items"),
    path("api/items_list", ItemListAPIView.as_view(), name="items_list"),
    path("api/sales_types", SalesTypeListAPIView.as_view(), name="sales_types"),
    path(
        "api/payments_methods",
        PaymentMethodListAPIView.as_view(),
        name="payments_methods",
    ),
    path("api/invoices", InvoiceHeaderApiView.as_view(), name="invoices"),
    path("api/invoices/", include("point_of_sales.urls")),
]
