from rest_framework import serializers
from .. import models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = "__all__"
        read_only_fields = ("id",)


class CustomerSomeFieldsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Customer
        fields = ["id", "name"]
        read_only_fields = ["name"]
