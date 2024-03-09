from django.urls import path
from .api import CustomerApiView


urlpatterns = [
    path("api/customers", CustomerApiView.as_view(), name="customers"),
]
