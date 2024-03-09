from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


class CustomerApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name", "phone", "email", "document_id"]

    def get(self, request):
        customer_id = request.query_params.get("customer_id", None)

        if customer_id:
            try:
                customer = self.queryset.get(pk=customer_id)
                serializer = self.serializer_class(customer)
                return Response(serializer.data)
            except models.Customer.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        customers_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(customers_list, many=True)
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
        customer_id = request.query_params.get("customer_id", None)

        if customer_id is None:
            return Response(
                "Debe suministrar el customer_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = self.queryset.get(pk=customer_id)
            serializer = self.serializer_class(customer, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Customer.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
