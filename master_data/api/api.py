from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


class DocumentTypeAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.DocumentTypeSerializer
    queryset = models.DocumentType.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]

    def get(self, request):
        document_type_id = request.query_params.get("document_type_id", None)

        if document_type_id:
            try:
                document_type = self.queryset.get(pk=document_type_id)
                serializer = self.serializer_class(document_type)
                return Response(serializer.data)
            except models.DocumentType.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        documents_types_list = self.queryset.all()
        serializer = self.serializer_class(documents_types_list, many=True)
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
        document_type_id = request.query_params.get("document_type_id", None)

        if document_type_id is None:
            return Response(
                "Debe suministrar el document_type_id",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            document_type = self.queryset.get(pk=document_type_id)
            serializer = self.serializer_class(document_type, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.DocumentType.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentTypeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.DocumentTypeSerializer
    queryset = models.DocumentType.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class TaxAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.TaxSerializer
    queryset = models.Tax.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]

    def get(self, request):
        tax_id = request.query_params.get("tax_id", None)

        if tax_id:
            try:
                tax = self.queryset.get(pk=tax_id)
                serializer = self.serializer_class(tax)
                return Response(serializer.data)
            except models.Tax.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        taxes_list = self.queryset.all()
        serializer = self.serializer_class(taxes_list, many=True)
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
        tax_id = request.query_params.get("tax_id", None)

        if tax_id is None:
            return Response(
                "Debe suministrar el tax_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            tax = self.queryset.get(pk=tax_id)
            serializer = self.serializer_class(tax, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Tax.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaxListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.TaxSerializer
    queryset = models.Tax.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class ReceiptAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.ReceiptSerializer
    queryset = models.Receipt.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name", "tax__name"]

    def get(self, request):
        receipt_id = request.query_params.get("receipt_id", None)

        if receipt_id:
            try:
                receipt = self.queryset.get(pk=receipt_id)
                serializer = self.serializer_class(receipt)
                return Response(serializer.data)
            except models.Receipt.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        receipts_list = self.queryset.all()
        serializer = self.serializer_class(receipts_list, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"{e}")
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        receipt_id = request.query_params.get("receipt_id", None)

        if receipt_id is None:
            return Response(
                "Debe suministrar el receipt_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receipt = self.queryset.get(pk=receipt_id)
            serializer = self.serializer_class(receipt, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Receipt.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceiptListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ReceiptReadSerializer
    queryset = models.Receipt.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class SalesTypeAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.SalesTypesSerializer
    queryset = models.SaleType.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]

    def get(self, request):
        sale_type_id = request.query_params.get("sale_type_id", None)

        if sale_type_id:
            try:
                sale_type = self.queryset.get(pk=sale_type_id)
                serializer = self.serializer_class(sale_type)
                return Response(serializer.data)
            except models.SaleType.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        sale_types_list = self.queryset.all()
        serializer = self.serializer_class(sale_types_list, many=True)
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
        sale_type_id = request.query_params.get("sale_type_id", None)

        if sale_type_id is None:
            return Response(
                "Debe suministrar el sale_type_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sale_type = self.queryset.get(pk=sale_type_id)
            serializer = self.serializer_class(sale_type, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.SaleType.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SalesTypeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SalesTypesReadSerializer
    queryset = models.SaleType.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class PaymentMethodAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]

    def get(self, request):
        payment_method_id = request.query_params.get("payment_method_id", None)

        if payment_method_id:
            try:
                tax = self.queryset.get(pk=payment_method_id)
                serializer = self.serializer_class(tax)
                return Response(serializer.data)
            except models.PaymentMethod.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        payments_methods_list = self.queryset.all()
        serializer = self.serializer_class(payments_methods_list, many=True)
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
        payment_method_id = request.query_params.get("payment_method_id", None)

        if payment_method_id is None:
            return Response(
                "Debe suministrar el payment_method_id",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment_method = self.queryset.get(pk=payment_method_id)
            serializer = self.serializer_class(payment_method, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.PaymentMethod.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentMethodListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PaymentMethodReadSerializer
    queryset = models.PaymentMethod.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class CompanyListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CompanyReadSerializer
    queryset = models.Company.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.first())
        return Response(serializer.data)
