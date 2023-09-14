from django.urls import path
from .views import print_invoice

urlpatterns = [path("print_invoice", print_invoice)]
