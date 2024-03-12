from rest_framework import serializers
from .. import models


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"
        read_only_fields = ("id",)


class ProviderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = ["id", "name"]
        read_only_fields = ("id", "name")
