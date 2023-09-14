from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.transaction import atomic
from .. import models
from . import serializers


# class LoginAPIView(generics.GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = serializers.LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         try:
#             if serializer.is_valid():
#                 login(request, serializer.validated_data)
#                 return Response({"is_login": True}, status=status.HTTP_200_OK)

#             return Response(status=status.HTTP_403_FORBIDDEN)
#         except:
#             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class LogoutAPIView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.LoginSerializer

#     def get(self, request):
#         logout(request)
#         return Response(status=status.HTTP_200_OK)


class DocumentTypeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.DocumentTypeSerializer
    queryset = models.DocumentType.objects.all()

    def get(self, request):
        document_type_id = request.query_params.get("document_type_id", None)

        if document_type_id:
            try:
                customer = self.queryset.get(pk=document_type_id)
                serializer = self.serializer_class(customer)
                return Response(serializer.data)
            except models.DocumentType.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        documents_types_list = self.queryset.all()
        serializer = self.serializer_class(documents_types_list, many=True)
        return Response(serializer.data)


class TaxListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.TaxSerializer
    queryset = models.Tax.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class ReceiptListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ReceiptSerializer
    queryset = models.Receipt.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


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


class ProviderApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.ProviderSerializer
    queryset = models.Provider.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name", "phone", "email", "document_id"]

    def get(self, request):
        provider_id = request.query_params.get("provider_id", None)
        not_paginated = request.query_params.get("not_paginated", None)

        if provider_id:
            try:
                provider = self.queryset.get(pk=provider_id)
                serializer = self.serializer_class(provider)
                return Response(serializer.data)
            except models.Provider.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        providers_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(providers_list, many=True)

        if not_paginated:
            return Response(serializer.data)

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
        provider_id = request.query_params.get("provider_id", None)

        if provider_id is None:
            return Response(
                "Debe suministrar el provider_id", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            provider = self.queryset.get(pk=provider_id)
            serializer = self.serializer_class(provider, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Provider.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class InvoiceHeaderApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.InvoiceHeaderSerializer
    queryset = models.InvoiceHeader.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "customer__name",
        "customer__phone",
        "customer__document_id",
        "receipt_type__name",
        "number",
    ]

    def get(self, request):
        invoice_header_id = request.query_params.get("invoice_header_id", None)

        if invoice_header_id:
            try:
                invoice_header = self.queryset.get(pk=invoice_header_id)
                serializer = self.serializer_class(invoice_header)
                return Response(serializer.data)
            except models.InvoiceHeader.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        invoices_headers_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(invoices_headers_list, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(user_created=request.user, user_updated=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        invoice_header_id = request.query_params.get("invoice_header_id", None)

        if invoice_header_id is None:
            return Response(
                "Debe suministrar el invoice_header_id",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            invoice_header = self.queryset.get(pk=invoice_header_id)
            serializer = self.serializer_class(invoice_header, data=request.data)

            if serializer.is_valid():
                serializer.save(user_updated=request.user)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.InvoiceHeader.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        invoice_header_id = request.query_params.get("invoice_header_id", None)
        try:
            with atomic():
                invoice_header_instance = self.queryset.get(pk=invoice_header_id)
                invoice_header_instance.inactivate()
                map(
                    lambda e: e.inactivate(),
                    invoice_header_instance.invoice_detail.all(),
                )
                map(lambda e: e.inanctivate(), invoice_header_instance.payment.all())
                return Response(status=status.HTTP_202_ACCEPTED)
        except models.InvoiceHeader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SalesTypeListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SalesTypesSerializer
    queryset = models.SaleType.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class PaymentMethodListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.queryset.filter(status=True), many=True)
        return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        permissions = user.get_all_permissions()

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "permissions": permissions,
            }
        )
