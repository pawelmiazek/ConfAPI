from rest_framework import serializers


class ConfiguratorSerializer(serializers.Serializer):
    base = serializers.JSONField()
    params = serializers.JSONField()
