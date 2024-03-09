from rest_framework import permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .. import models
from . import serializers


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
