from rest_framework import serializers
from django.db.transaction import atomic
from django.db import IntegrityError
from .. import models


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = "__all__"
        read_only_fields = ("id", "name")


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tax
        fields = "__all__"
        read_only_fields = ["id", "name", "percentage", "status"]


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receipt
        fields = ["id", "name", "serial", "expiration"]
        read_only_fields = ["id", "name", "serial", "expiration"]


class SomeFieldsSequenceReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SequenceReceipt
        fields = [
            "id",
            "sequence",
        ]
        read_only_fields = [
            "id",
            "sequence",
        ]


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


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"
        read_only_fields = ("id",)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"
        read_only_fields = (
            "id",
            "stock",
        )


class SomeFieldItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Item
        fields = ["id", "name"]
        read_only_fields = ["name"]


class ItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "name", "price", "tax"]
        read_only_fields = ["id", "name", "price", "tax"]


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("invoice",)


class InvoiceDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    item = SomeFieldItemSerializer(required=True)

    class Meta:
        model = models.InvoiceDetail
        fields = "__all__"
        read_only_fields = ("invoice_header",)


class InvoiceHeaderSerializer(serializers.ModelSerializer):
    invoice_detail = InvoiceDetailSerializer(required=True, many=True)
    payment = PaymentSerializer(required=False, many=True)
    customer = CustomerSomeFieldsSerializer(required=True)
    sequence_receipt = SomeFieldsSequenceReceiptSerializer(read_only=True)
    invoice_detail_to_delete = serializers.ListField(
        child=serializers.JSONField(), required=False, write_only=True
    )

    class Meta:
        model = models.InvoiceHeader
        fields = "__all__"
        read_only_fields = (
            "id",
            "number",
            "sequence_receipt",
            "user_created",
            "user_updated",
            "date_created",
            "date_updated",
        )

    def _create_invoice_details(
        self, invoice_header_instance, invoice_details_datalist
    ):
        for invoice_detail_data in invoice_details_datalist:
            item_data = invoice_detail_data.pop("item")
            invoice_detail_data.pop("id")
            invoice_detail_instance = invoice_header_instance.invoice_detail.create(
                item_id=item_data["id"], **invoice_detail_data
            )
            invoice_detail_instance.item.decrease_stock(invoice_detail_data["quantity"])

    def _create_payments(self, invoice_header_instance, payments_datalist):
        for payment_data in payments_datalist:
            payment_data.pop("id")
            invoice_header_instance.payment.create(**payment_data)

    def _create_sequence_receipt(self, receipt):
        sequence_receipt = models.SequenceReceipt.objects.filter(
            to_reuse=True, receipt=receipt
        ).first()
        if sequence_receipt is not None:
            sequence_receipt.unmark_to_reuse()
            return sequence_receipt

        return models.SequenceReceipt.objects.create(receipt=receipt)

    def _update_invoice_details(self, invoice_header_instance, invoice_details_list):
        for invoice_detail in invoice_details_list:
            if invoice_detail["id"].isnumeric():
                invoice_detail_instance = models.InvoiceDetail.objects.get(
                    pk=invoice_detail["id"], invoice_header=invoice_header_instance
                )
                if invoice_detail.get("quantity") > invoice_detail_instance.quantity:
                    quantity_decrease_stock = (
                        invoice_detail.get("quantity")
                        - invoice_detail_instance.quantity
                    )
                    invoice_detail_instance.item.decrease_stock(quantity_decrease_stock)
                elif invoice_detail.get("quantity") < invoice_detail_instance.quantity:
                    quantity_increase_stock = (
                        invoice_detail_instance.quantity
                        - invoice_detail.get("quantity")
                    )
                    invoice_detail_instance.item.increase_stock(quantity_increase_stock)

                invoice_detail_instance.quantity = invoice_detail.get(
                    "quantity", invoice_detail_instance.quantity
                )
                invoice_detail_instance.price = invoice_detail.get(
                    "price", invoice_detail_instance.price
                )
                invoice_detail_instance.tax = invoice_detail.get(
                    "tax", invoice_detail_instance.tax
                )
                invoice_detail_instance.discount = invoice_detail.get(
                    "discount", invoice_detail_instance.discount
                )

                invoice_detail_instance.save()
            else:
                invoice_detail.pop("id")
                item_data = invoice_detail.pop("item")
                invoice_detail_instance = invoice_header_instance.invoice_detail.create(
                    item_id=item_data["id"], **invoice_detail
                )
                invoice_detail_instance.item.decrease_stock(
                    invoice_detail_instance.quantity
                )

    def _delete_invoice_details(self, invoice_header_instance, invoice_details_list):
        for invoice_detail in invoice_details_list:
            invoice_detail_instance = models.InvoiceDetail.objects.get(
                pk=invoice_detail["id"],
                invoice_header=invoice_header_instance,
            )
            invoice_detail_instance.delete()

    def create(self, validated_data):
        try:
            with atomic():
                invoice_details_data = validated_data.pop("invoice_detail")
                customer_data = validated_data.pop("customer")
                payments_data = validated_data.pop("payment")

                if validated_data["receipt_type"].id != 1:
                    validated_data["sequence_receipt"] = self._create_sequence_receipt(
                        validated_data["receipt_type"]
                    )

                invoice_header = models.InvoiceHeader.objects.create(
                    customer_id=customer_data["id"],
                    **validated_data,
                )

                if invoice_details_data is not None:
                    self._create_invoice_details(invoice_header, invoice_details_data)
                else:
                    raise Exception("La factura debe tener al menos un detalle.")

                if payments_data is not None:
                    self._create_payments(invoice_header, payments_data)

            return invoice_header
        except Exception as e:
            print("#### InvoiceHeaderSerializer > create: \n", e)
            return e

    def update(self, instance, validated_data):
        try:
            with atomic():
                validated_data.pop("receipt_type")
                invoice_details_data = validated_data.pop("invoice_detail")
                customer_data = validated_data.pop("customer")

                invoice_details_to_delete_data = (
                    validated_data.pop("invoice_detail_to_delete")
                    if validated_data.get("invoice_detail_to_delete", None)
                    else None
                )

                instance.comment = validated_data.get("comment", instance.comment)
                instance.discount = validated_data.get("discount", instance.discount)
                instance.sales_type = validated_data.get(
                    "sales_type", instance.sales_type
                )
                instance.user_updated = validated_data.get(
                    "user_updated", instance.user_updated
                )

                instance.customer = models.Customer.objects.get(pk=customer_data["id"])

                if invoice_details_to_delete_data is not None:
                    self._delete_invoice_details(
                        instance, invoice_details_to_delete_data
                    )

                if invoice_details_data:
                    self._update_invoice_details(instance, invoice_details_data)

                instance.save()
                return instance
        except models.InvoiceHeader.DoesNotExist as e:
            print("#### InvoiceHeaderSerializer > update > DoesNotExist: \n", e)
            return e
        except IntegrityError as e:
            print("#### InvoiceHeaderSerializer > update > IntegrityError: \n", e)
            return e
        except Exception as e:
            print("#### InvoiceHeaderSerializer > update > Exception: \n", e)
            return e


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentMethod
        fields = "__all__"
        read_only_fields = ("id", "name", "status")


class SalesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleType
        fields = "__all__"
        read_only_fields = ("id", "name", "status")
