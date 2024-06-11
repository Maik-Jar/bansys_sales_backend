from rest_framework import serializers
from django.contrib.auth.models import User
from .. import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = "__all__"
        read_only_fields = ("id",)


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = "__all__"
        read_only_fields = ("id",)


class TaxReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = ["id", "name", "percentage"]
        read_only_fields = ("id",)


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = "__all__"
        read_only_fields = ("id",)


class ReceiptReadSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(read_only=True)

    class Meta:
        model = models.Receipt
        fields = "__all__"
        read_only_fields = ("id",)


class SomeFieldsReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Receipt
        fields = ("id",)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = "__all__"
        read_only_fields = ("id",)


class PaymentMethodReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = "__all__"
        read_only_fields = ("id", "name", "status")


class SalesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleType
        fields = "__all__"
        read_only_fields = ("id",)


class SalesTypesReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleType
        fields = "__all__"
        read_only_fields = ("id", "name", "status")


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = "__all__"
        read_only_fields = ("id",)


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = "__all__"
        read_only_fields = ("id",)


class ConditionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = "__all__"
        read_only_fields = ("id", "name", "description", "status")
