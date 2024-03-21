from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


class InputApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.InputAPISerializer
    queryset = models.Input.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["item__name", "purchase_order", "invoice_number", "provider__name"]

    def get(self, request):
        input_id = request.query_params.get("input_id", None)

        if input_id:
            try:
                input_instance = self.queryset.get(pk=input_id)
                serializer = self.serializer_class(input_instance)
                return Response(serializer.data)
            except models.Input.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        input_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(input_list, many=True)
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
        input_id = request.query_params.get("input_id", None)

        if input_id is None:
            return Response(
                "Debe suministrar el input_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            input_instance = self.queryset.get(pk=input_id)
            serializer = self.serializer_class(input_instance, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Input.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutputApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.OutputAPISerializer
    queryset = models.Output.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "item__name",
    ]

    def get(self, request):
        output_id = request.query_params.get("output_id", None)

        if output_id:
            try:
                output = self.queryset.get(pk=output_id)
                serializer = self.serializer_class(output)
                return Response(serializer.data)
            except models.Output.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        outputs_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(outputs_list, many=True)
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
        output_id = request.query_params.get("output_id", None)

        if output_id is None:
            return Response(
                "Debe suministrar el output_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            output_instance = self.queryset.get(pk=output_id)
            serializer = self.serializer_class(output_instance, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Output.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
