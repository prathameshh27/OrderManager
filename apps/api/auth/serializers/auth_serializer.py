from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False)