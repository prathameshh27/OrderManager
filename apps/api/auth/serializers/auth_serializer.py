from rest_framework import serializers

class TokenPairSerializer(serializers.Serializer):
    """Validates the request obtained for retriving the Bearer Token"""
    username = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False)


class RefreshTokenSerializer(serializers.Serializer):
    """Validates the request obtained for retriving the access Token"""
    refresh_token = serializers.CharField(required=True, allow_null=False)


class AccessTokenResSerializer(serializers.Serializer):
    """Response containing the access token and the validity"""
    token = serializers.CharField(read_only=True)
    valid_upto = serializers.CharField(read_only=True)


class RefreshTokenResSerializer(serializers.Serializer):
    """Response containing the refresh token and the validity"""
    token = serializers.CharField(read_only=True)
    valid_upto = serializers.CharField(read_only=True)


class TokenPairResSerializer(serializers.Serializer):
    """Response containing the both refresh and access token along with their validity"""
    refresh_token = RefreshTokenResSerializer(read_only=True)
    access_token = AccessTokenResSerializer(read_only=True)