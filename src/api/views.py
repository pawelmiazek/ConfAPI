from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import ConfiguratorSerializer


class ConfiguratorView(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = ConfiguratorSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
