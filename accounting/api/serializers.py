from rest_framework import serializers
from .. import models


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("invoice",)
