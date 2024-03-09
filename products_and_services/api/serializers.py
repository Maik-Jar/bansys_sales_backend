from rest_framework import serializers
from .. import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"
        read_only_fields = (
            "id",
            "stock",
        )


class SomeFieldItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Item
        fields = ["id", "name"]
        read_only_fields = ["name"]


class ItemsListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        price = float(data["price"])
        discount = float(data["discount"])

        if discount > 0:
            data["price"] = str(
                price - (price * discount) if 0 < discount < 1 else price - discount
            )

        data.pop("discount")
        return data

    class Meta:
        model = models.Item
        fields = ["id", "name", "price", "discount"]
        read_only_fields = ["id", "name", "price", "discount"]
