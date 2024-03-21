from rest_framework import serializers
from .. import models
from products_and_services.api.serializers import SomeFieldItemSerializer
from products_and_services.models import Item


class InputAPISerializer(serializers.ModelSerializer):
    item = SomeFieldItemSerializer(required=True)

    class Meta:
        model = models.Input
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        try:
            validated_data["item"] = Item.objects.get(pk=validated_data["item"]["id"])
            return super().create(validated_data)
        except Exception as e:
            print("#### InputAPISerializer > create: \n", e)
            return e

    def update(self, instance, validated_data):
        try:
            validated_data["item"] = Item.objects.get(pk=validated_data["item"]["id"])
            print(validated_data)
            return super().update(instance, validated_data)
        except Exception as e:
            print("#### InputAPISerializer > update: \n", e)
            return e


class OutputAPISerializer(serializers.ModelSerializer):
    item = SomeFieldItemSerializer(required=True)

    class Meta:
        model = models.Output
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        try:
            validated_data["item"] = Item.objects.get(pk=validated_data["item"]["id"])
            return super().create(validated_data)
        except Exception as e:
            print("#### OutputAPISerializer > create: \n", e)
            return e

    def update(self, instance, validated_data):
        try:
            validated_data["item"] = Item.objects.get(pk=validated_data["item"]["id"])
            return super().update(instance, validated_data)
        except Exception as e:
            print("#### OutputAPISerializer > update: \n", e)
            return e
