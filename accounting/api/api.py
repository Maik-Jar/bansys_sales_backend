from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User
from .. import models
from . import serializers


class PaymentApiView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions | permissions.IsAdminUser,
    ]
    serializer_class = serializers.PaymentSerializerAPIView
    queryset = models.Payment.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "invoice__number",
        "invoice__customer__name",
    ]

    def get(self, request):
        payment_id = request.query_params.get("payment_id", None)

        if payment_id:
            try:
                payment = self.queryset.get(pk=payment_id)
                serializer = self.serializer_class(payment)
                return Response(serializer.data)
            except models.Payment.DoesNotExist as e:
                return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)

        payments_list = self.filter_queryset(self.queryset.all())
        serializer = self.serializer_class(payments_list, many=True)
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
        payment_id = request.query_params.get("payment_id", None)

        if payment_id is None:
            return Response(
                "Debe suministrar el payment_id",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = self.queryset.get(pk=payment_id)
            serializer = self.serializer_class(payment, data=request.data)

            if serializer.is_valid():
                serializer.save(user_updated=request.user)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Payment.DoesNotExist as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        payment_id = request.query_params.get("payment_id", None)
        try:
            payment_instance = self.queryset.get(pk=payment_id)

            if payment_instance.status:
                user_instance = User.objects.get(pk=request.user.id)
                payment_instance.inactivate(
                    request.data["inactivate_comment"], user_instance
                )
                return Response(status=status.HTTP_202_ACCEPTED)

            return Response(
                "Esta pago ya esta inactivado.", status=status.HTTP_400_BAD_REQUEST
            )
        except models.Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
