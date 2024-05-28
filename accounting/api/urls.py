from django.urls import path, include
from .api import PaymentApiView

urlpatterns = [
    path("api/payments", PaymentApiView.as_view()),
    # path("api/print/", include("accounting.urls")),
]
