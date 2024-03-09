from django.urls import path
from .api import (
    ItemApiView,
    ItemListAPIView,
)

urlpatterns = [
    path("api/items", ItemApiView.as_view(), name="items"),
    path("api/items_list", ItemListAPIView.as_view(), name="items_list"),
]
