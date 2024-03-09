from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


class ItemApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.ItemSerializer
    queryset = models.Item.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name", "brand", "reference", "provider__name"]

    def get(self, request):
        item_id = request.query_params.get("item_id", None)

        if item_id:
            try:
                item = self.queryset.get(pk=item_id)
                serializer = self.serializer_class(item)
                return Response(serializer.data)
            except models.Item.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        items_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(items_list, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        item_id = request.query_params.get("item_id", None)

        if item_id is None:
            return Response(
                "Debe suministrar el item_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = self.queryset.get(pk=item_id)
            serializer = self.serializer_class(item, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Item.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ItemsListSerializer
    queryset = models.Item.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)
