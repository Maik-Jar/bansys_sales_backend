from django.urls import path
from .api import InputApiView, OutputApiView

urlpatterns = [
    path("api/inputs", InputApiView.as_view()),
    path("api/outputs", OutputApiView.as_view()),
]
