from rest_framework import serializers
from django.db.transaction import atomic
from django.db import IntegrityError
from django.utils import timezone
from sequences import Sequence
from .. import models


def sequence_generated(name):
    return next(Sequence(sequence_name=name))


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
        read_only_fields = "invoice_header"


class InvoiceDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    item = SomeFieldItemSerializer(required=True)

    class Meta:
        model = models.InvoiceDetail
        fields = "__all__"
        read_only_fields = ("invoice_header",)


class InvoiceHeaderSerializer(serializers.ModelSerializer):
    invoice_detail = InvoiceDetailSerializer(required=True, many=True)
    payment = PaymentSerializer(required=True, many=True)
    customer = CustomerSomeFieldsSerializer(required=True)
    invoice_detail_to_delete = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
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

    def create(self, validated_data):
        invoice_details_data = validated_data.pop("invoice_detail")
        customer_data = validated_data.pop("customer")
        payments_data = validated_data.pop("payment")

        try:
            with atomic():
                if validated_data["receipt_type"].id != 1:
                    validated_data[
                        "sequence_receipt"
                    ] = models.SequenceReceipt.objects.create(
                        receipt=validated_data["receipt_type"],
                        sequence=sequence_generated(
                            f"{validated_data['receipt_type'].serial}"
                        ),
                    )

                invoive_number = f"{timezone.now().year}" + str(
                    sequence_generated(f"invoice_number-{timezone.now().year}")
                ).zfill(5)

                invoice_header = models.InvoiceHeader.objects.create(
                    number=invoive_number,
                    customer_id=customer_data["id"],
                    **validated_data,
                )

                if invoice_details_data is not None:
                    for invoice_detail_data in invoice_details_data:
                        item_data = invoice_detail_data.pop("item")
                        invoice_detail_instance = invoice_header.invoice_detail.create(
                            item_id=item_data["id"], **invoice_detail_data
                        )
                        invoice_detail_instance.item.decrease_stock(
                            invoice_detail_data["quantity"]
                        )
                else:
                    raise Exception("La factura debe tener al menos un detalle.")

                if payment_data is not None:
                    for payment_data in payments_data:
                        invoice_header.payment.create(**payment_data)

            return invoice_header
        except Exception as e:
            print("#### InvoiceHeaderSerializer > create: \n", e)
            return e

    def update(self, instance, validated_data):
        invoice_details_data = validated_data.pop("invoice_detail")
        customer_data = validated_data.pop("customer")
        validated_data.pop("payment")

        invoice_details_to_delete_data = (
            validated_data.pop("invoice_detail_to_delete")
            if validated_data.get("invoice_detail_to_delete", None)
            else None
        )
        try:
            instance.customer = models.Customer.objects.get(pk=customer_data["id"])
        except models.Customer.DoesNotExist:
            pass

        instance.subtotal = validated_data.get("subtotal", instance.subtotal)
        instance.total_tax = validated_data.get("total_tax", instance.total_tax)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.total = validated_data.get("total", instance.total)
        instance.paid = validated_data.get("paid", instance.paid)
        instance.payment_method = validated_data.get(
            "payment_method", instance.payment_method
        )
        instance.sales_type = validated_data.get("sales_type", instance.sales_type)
        instance.user_updated = validated_data.get(
            "user_updated", instance.user_updated
        )
        instance.status = validated_data.get("status", instance.status)

        try:
            with atomic():
                if invoice_details_to_delete_data is not None:
                    for invoice_detail_to_delete_data in invoice_details_to_delete_data:
                        invoice_detail_instance = models.InvoiceDetail.objects.get(
                            pk=invoice_detail_to_delete_data,
                            invoice_header=instance,
                        )
                        invoice_detail_instance.item.increase_stock(
                            invoice_detail_instance.quantity
                        )
                        invoice_detail_instance.delete()

                if invoice_details_data:
                    for invoice_detail_data in invoice_details_data:
                        if invoice_detail_data["id"].isnumeric():
                            invoice_detail_instance = models.InvoiceDetail.objects.get(
                                pk=invoice_detail_data["id"], invoice_header=instance
                            )
                            if (
                                invoice_detail_data.get("quantity")
                                > invoice_detail_instance.quantity
                            ):
                                quantity_decrease_stock = (
                                    invoice_detail_data.get("quantity")
                                    - invoice_detail_instance.quantity
                                )
                                invoice_detail_instance.item.decrease_stock(
                                    quantity_decrease_stock
                                )
                            elif (
                                invoice_detail_data.get("quantity")
                                < invoice_detail_instance.quantity
                            ):
                                quantity_increase_stock = (
                                    invoice_detail_instance.quantity
                                    - invoice_detail_data.get("quantity")
                                )
                                invoice_detail_instance.item.increase_stock(
                                    quantity_increase_stock
                                )

                            invoice_detail_instance.quantity = invoice_detail_data.get(
                                "quantity", invoice_detail_instance.quantity
                            )
                            invoice_detail_instance.price = invoice_detail_data.get(
                                "price", invoice_detail_instance.price
                            )
                            invoice_detail_instance.tax = invoice_detail_data.get(
                                "tax", invoice_detail_instance.tax
                            )
                            invoice_detail_instance.discount = invoice_detail_data.get(
                                "discount", invoice_detail_instance.discount
                            )

                            invoice_detail_instance.save()
                        else:
                            invoice_detail_data.pop("id")
                            invoice_detail_instance = instance.invoice_detail.create(
                                **invoice_detail_data
                            )
                            invoice_detail_instance.item.decrease_stock(
                                invoice_detail_instance.quantity
                            )
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
