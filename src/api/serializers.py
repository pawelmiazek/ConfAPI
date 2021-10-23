from rest_framework import serializers
from nested_lookup import get_all_keys, nested_lookup, nested_update
import json


class ConfiguratorSerializer(serializers.Serializer):
    base = serializers.JSONField(write_only=True)
    params = serializers.JSONField(write_only=True)

    def validate(self, attrs):
        base = attrs.get("base")
        params = attrs.get("params")
        base_keys = get_all_keys(base)
        params_keys = get_all_keys(params)

        not_found_params = [param for param in params_keys if param not in base_keys]
        if not_found_params:
            raise serializers.ValidationError(f"Wrong params config file. These params do not exist in base file: {not_found_params}")
        return super().validate(attrs)

    def create(self, validated_data):
        base = validated_data.pop("base")
        params = validated_data.pop("params")
        params_keys = get_all_keys(params)
        result = []
        
        changed_key_values = [key for key in params_keys if isinstance(nested_lookup(key, params)[0], list)]

        for key in changed_key_values:
            for value in nested_lookup(key, params)[0]:

                new_configuration = nested_update(base, key=key, value=value)
                result.append(new_configuration)

        return result
