from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from point_of_sales.models import Customer
from django.contrib.auth.models import User
import base64


class CustomerApiTest(APITestCase):
    def test_create_user(self):
        credentials = "brivera:frente21"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {base64_credentials}")

        url = reverse("customers")
        data = {
            "name": "Miguelina Luciano SRL",
            "document_type": 3,
            "document_id": "123456789",
            "phone": "1234567890",
        }
        response = self.client.post(
            "localhost:8000//point_of_sales/api/customers", data, format="json"
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, "Miguelina Luciano SRL")
