from django.urls import path
from .api import ProviderApiView, ProviderListAPIView

urlpatterns = [
    path("api/providers", ProviderApiView.as_view(), name="providers"),
    path("api/providers_list", ProviderListAPIView.as_view()),
]
