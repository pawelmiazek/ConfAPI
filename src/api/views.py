from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import ConfiguratorSerializer


class ConfiguratorView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfiguratorSerializer

    def post(self, request, *args, **kwargs):
        serializer = ConfiguratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.instance, status=status.HTTP_200_OK)
