from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


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
