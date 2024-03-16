from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.transaction import atomic
from django.contrib.auth.models import User
from .. import models
from . import serializers


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
                user_instance = User.objects.get(pk=request.user.id)

                invoice_header_instance = self.queryset.get(pk=invoice_header_id)
                invoice_header_instance.inactivate(
                    request.data["inactivate_comment"], user_instance
                )
                map(
                    lambda e: e.inactivate(),
                    invoice_header_instance.invoice_detail.all(),
                )
                map(
                    lambda e: e.inactivate(
                        request.data["inactivate_comment"], user_instance
                    ),
                    invoice_header_instance.payment.all(),
                )

                try:
                    receipt_sequence_instance = models.SequenceReceipt.objects.get(
                        invoice=invoice_header_instance
                    )
                except:
                    receipt_sequence_instance = None

                if receipt_sequence_instance is not None:
                    receipt_sequence_instance.inactivate()

                return Response(status=status.HTTP_202_ACCEPTED)
        except models.InvoiceHeader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InvoiceHeaderListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.InvoiceHeaderReadSerializer
    queryset = models.InvoiceHeader.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "customer__name",
        "customer__phone",
        "customer__document_id",
        "number",
    ]

    def get(self, request):
        invoices_headers_list = self.filter_queryset(
            self.queryset.filter(status=True, pending_payment=True)
        )
        serializer = self.serializer_class(invoices_headers_list, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class QuotationHeaderApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.QuotationHeaderSerializer
    queryset = models.QuotationHeader.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "customer__name",
        "customer__phone",
        "customer__document_id",
        "number",
    ]

    def get(self, request):
        quotation_header_id = request.query_params.get("quotation_header_id", None)

        if quotation_header_id:
            try:
                quotation_header = self.queryset.get(pk=quotation_header_id)
                serializer = self.serializer_class(quotation_header)
                return Response(serializer.data)
            except models.QuotationHeader.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        quotations_headers_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(quotations_headers_list, many=True)
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
        quotation_header_id = request.query_params.get("quotation_header_id", None)

        if quotation_header_id is None:
            return Response(
                "Debe suministrar el quotation_header_id",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quotation_header = self.queryset.get(pk=quotation_header_id)
            serializer = self.serializer_class(quotation_header, data=request.data)

            if serializer.is_valid():
                serializer.save(user_updated=request.user)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.QuotationHeader.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        quotation_header_id = request.query_params.get("quotation_header_id", None)
        try:
            with atomic():
                quotation_header_instance = self.queryset.get(pk=quotation_header_id)
                quotation_header_instance.inactivate()

                return Response(status=status.HTTP_202_ACCEPTED)
        except models.QuotationHeader.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
