from rest_framework import serializers
from master_data.api.serializers import UserSerializer
from .. import models


class PaymentSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("id", "invoice")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["invoice"] = instance.invoice.number

        return data


class PaymentSerializerAPIView(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    invoice_number = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("id", "invoice_number")

    def update(self, instance, validated_data):
        validated_data["amount"] = instance.amount
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        instance.invoice_number = instance.invoice.number
        return super().to_representation(instance)
