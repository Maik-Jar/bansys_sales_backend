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
        read_only_fields = ["id"]


class ReceiptSerializer(serializers.ModelSerializer):
    tax = TaxSerializer(read_only=True)

    class Meta:
        model = models.Receipt
        fields = "__all__"
        read_only_fields = ["id"]


class SomeFieldsReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Receipt
        fields = [
            "id",
        ]


class SequenceReceiptSerializer(serializers.ModelSerializer):
    receipt = ReceiptSerializer(read_only=True)

    class Meta:
        model = models.SequenceReceipt
        fields = "__all__"
        read_only_fields = ["id", "sequence"]


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
        fields = ["id", "name", "price"]
        read_only_fields = ["id", "name", "price"]


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("invoice",)


class QuotationDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    item = SomeFieldItemSerializer(required=True)

    class Meta:
        model = models.QuotationDetail
        fields = "__all__"
        read_only_fields = ("quotation_header",)


class QuotationHeaderSerializer(serializers.ModelSerializer):
    quotation_detail = QuotationDetailSerializer(required=True, many=True)
    # customer = CustomerSomeFieldsSerializer(required=False)
    quotation_detail_to_delete = serializers.ListField(
        child=serializers.JSONField(), required=False, write_only=True
    )

    class Meta:
        model = models.QuotationHeader
        fields = "__all__"
        read_only_fields = (
            "id",
            "number",
            "user_created",
            "user_updated",
            "date_created",
            "date_updated",
        )

    def _create_quotation_details(
        self, quotation_header_instance, quotation_details_datalist
    ):
        for quotation_detail_data in quotation_details_datalist:
            item_data = quotation_detail_data.pop("item")
            quotation_detail_data.pop("id")
            quotation_header_instance.quotation_detail.create(
                item_id=item_data["id"], **quotation_detail_data
            )

    def _update_quotation_details(
        self, quotation_header_instance, quotation_details_list
    ):
        for quotation_detail in quotation_details_list:
            if quotation_detail["id"].isnumeric():
                quotation_detail_instance = models.QuotationDetail.objects.get(
                    pk=quotation_detail["id"],
                    quotation_header=quotation_header_instance,
                )

                quotation_detail_instance.quantity = quotation_detail.get(
                    "quantity", quotation_detail_instance.quantity
                )
                quotation_detail_instance.price = quotation_detail.get(
                    "price", quotation_detail_instance.price
                )
                quotation_detail_instance.tax = quotation_detail.get(
                    "tax", quotation_detail_instance.tax
                )
                quotation_detail_instance.discount = quotation_detail.get(
                    "discount", quotation_detail_instance.discount
                )

                quotation_detail_instance.save()
            else:
                quotation_detail.pop("id")
                item_data = quotation_detail.pop("item")
                quotation_detail_instance = (
                    quotation_header_instance.quotation_detail.create(
                        item_id=item_data["id"], **quotation_detail
                    )
                )

    def _delete_quotation_details(
        self, quotation_header_instance, quotation_details_list
    ):
        for quotation_detail in quotation_details_list:
            quotation_detail_instance = models.QuotationDetail.objects.get(
                pk=quotation_detail["id"],
                quotation_header=quotation_header_instance,
            )
            quotation_detail_instance.delete()

    def create(self, validated_data):
        try:
            with atomic():
                quotation_details_data = validated_data.pop("quotation_detail")
                # customer_data = (
                #     validated_data.pop("customer")
                #     if validated_data.get("customer")
                #     else None
                # )

                # quotation_header = (
                #     models.QuotationHeader.objects.create(
                #         customer_id=customer_data["id"], **validated_data
                #     )
                #     if customer_data
                #     else models.QuotationHeader.objects.create(**validated_data)
                # )

                quotation_header = models.QuotationHeader.objects.create(
                    **validated_data
                )

                if quotation_details_data is not None:
                    self._create_quotation_details(
                        quotation_header, quotation_details_data
                    )
                else:
                    raise Exception("La cotización debe tener al menos un detalle.")

            return quotation_header
        except Exception as e:
            print("#### QuotationHeaderSerializer > create: \n", e)
            return e

    def update(self, instance, validated_data):
        try:
            with atomic():
                quotation_details_data = validated_data.pop("quotation_detail")
                # customer_data = (
                #     validated_data.pop("customer")
                #     if validated_data.get("customer")
                #     else None
                # )
                quotation_details_to_delete_data = (
                    validated_data.pop("quotation_detail_to_delete")
                    if validated_data.get("quotation_detail_to_delete", None)
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
                instance.customer = validated_data.get("customer", instance.customer)

                # if customer_data:
                #     instance.customer = models.Customer.objects.get(
                #         pk=customer_data["id"]
                #     )

                if quotation_details_to_delete_data is not None:
                    self._delete_quotation_details(
                        instance, quotation_details_to_delete_data
                    )

                if quotation_details_data:
                    self._update_quotation_details(instance, quotation_details_data)

                instance.save()
                return instance
        except models.QuotationHeader.DoesNotExist as e:
            print("#### QuotationHeaderSerializer > update > DoesNotExist: \n", e)
            return e
        except IntegrityError as e:
            print("#### QuotationHeaderSerializer > update > IntegrityError: \n", e)
            return e
        except Exception as e:
            print("#### QuotationHeaderSerializer > update > Exception: \n", e)
            return e


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
    receipt_sequence = SequenceReceiptSerializer(read_only=True)
    receipt = SomeFieldsReceiptSerializer(required=True, write_only=True)
    invoice_detail_to_delete = serializers.ListField(
        child=serializers.JSONField(), required=False, write_only=True
    )

    class Meta:
        model = models.InvoiceHeader
        fields = "__all__"
        read_only_fields = (
            "id",
            "number",
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

    def _create_sequence_receipt(self, receipt, invoice_instance):
        sequence_receipt = models.SequenceReceipt.objects.filter(
            to_reuse=True, receipt_id=receipt["id"], invoice__isnull=True
        ).first()
        if sequence_receipt is not None:
            sequence_receipt.unmark_to_reuse(invoice_instance)
            return sequence_receipt

        return models.SequenceReceipt.objects.create(
            receipt_id=receipt["id"], invoice=invoice_instance
        )

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
                # invoice_detail_instance.tax = invoice_detail.get(
                #     "tax", invoice_detail_instance.tax
                # )
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
                receipt_data = validated_data.pop("receipt")

                receipt_instance = models.Receipt.objects.get(id=receipt_data["id"])

                invoice_header = models.InvoiceHeader.objects.create(
                    customer_id=customer_data["id"],
                    tax=(receipt_instance.tax.percentage / 100),
                    **validated_data,
                )

                if receipt_data["id"] != 1:
                    self._create_sequence_receipt(receipt_data, invoice_header)

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
                validated_data.pop("receipt")
                invoice_details_data = validated_data.pop("invoice_detail")
                customer_data = validated_data.pop("customer")

                invoice_details_to_delete_data = (
                    validated_data.pop("invoice_detail_to_delete")
                    if validated_data.get("invoice_detail_to_delete", None)
                    else None
                )

                instance.comment = validated_data.get("comment", instance.comment)
                instance.discount = validated_data.get("discount", instance.discount)
                instance.avance = validated_data.get("avance", instance.avance)
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
