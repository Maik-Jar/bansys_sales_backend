from django.urls import path
from .api import ProviderApiView

urlpatterns = [
    path("api/providers", ProviderApiView.as_view(), name="providers"),
]
