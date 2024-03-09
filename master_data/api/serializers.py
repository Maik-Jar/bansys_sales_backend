from rest_framework import serializers
from .. import models


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = "__all__"
        read_only_fields = ("id", "name")


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = "__all__"
        read_only_fields = ["id"]


class ReceiptSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(read_only=True)

    class Meta:
        model = models.Receipt
        fields = "__all__"
        read_only_fields = ["id"]


class SomeFieldsReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Receipt
        fields = [
            "id",
        ]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = "__all__"
        read_only_fields = ("id", "name", "status")


class SalesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleType
        fields = "__all__"
        read_only_fields = ("id", "name", "status")
