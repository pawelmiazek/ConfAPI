from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import ConfiguratorSerializer


response_schema_dict = {
    "200": openapi.Response(
        description="200",
        examples={
            "application/json": {
                "results": [],
            }
        }
    )
}


class ConfiguratorView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfiguratorSerializer

    @swagger_auto_schema(
        request_body=ConfiguratorSerializer,
        responses=response_schema_dict
    )
    def post(self, request, *args, **kwargs):
        serializer = ConfiguratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.instance, status=status.HTTP_200_OK)
