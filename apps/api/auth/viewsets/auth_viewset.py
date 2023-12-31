from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from ..serializers.auth_serializer import (
    TokenPairResSerializer, AccessTokenResSerializer, 
    TokenPairSerializer, RefreshTokenSerializer)



IST_TZ = getattr(settings, 'IST_TZ', None)


class TokenPairSpecs:
    """OpenAPI specifications for the Auth Token API endpoints"""
    create = {
        "request": TokenPairSerializer, 
        "responses": TokenPairResSerializer,
        "description": """<h2>Get bearer token</h2>
                        Allows the user to retrive a bearer token for accessing the API endpoints.
                        Accepts username and password.""",
    }


class AccessTokenSpecs:
    """OpenAPI specifications for the Refresh Token API endpoints"""
    create = {
        "request": RefreshTokenSerializer, 
        "responses": AccessTokenResSerializer,
        "description": """<h2>Refresh access token</h2>
                        Allows the user to refresh the short persistent access token for accessing the API endpoints.
                        Accepts a Refresh token previously obtained from Auth token API endpoint.""",
    }




class ObtainTokenPair(viewsets.ViewSet):
    """Authentication API"""
    
    page_name = None

    def get_view_name(self):
        return self.page_name

    @extend_schema(**TokenPairSpecs.create,)
    def create(self, request):
        """Login - POST Endpoint"""

        self.page_name = "Get Bearer Token"
        post_data = request.data

        login_serializer = TokenPairSerializer(data=post_data)
        login_serializer.is_valid(raise_exception=True)

        username = login_serializer.data.get('username')
        password = login_serializer.data.get('password')

        user_instance = authenticate(username=username, password=password)
        print(user_instance)

        if user_instance is not None:
            refresh_token = RefreshToken.for_user(user=user_instance)
            refresh_validity = refresh_token.current_time + refresh_token.lifetime 
            
            access_token = refresh_token.access_token
            access_validity = access_token.current_time + access_token.lifetime 

            if IST_TZ is not None:
                refresh_validity = refresh_validity.astimezone(IST_TZ)
                access_validity = access_validity.astimezone(IST_TZ)

            return Response({
                'refresh_token': {
                    'token': str(refresh_token),
                    'valid_upto' : str(refresh_validity)
                },
                'access_token' : {
                    'token': str(access_token),
                    'valid_upto' : str(refresh_validity)
                }
            }, 200)
        
        else:
            return Response({
                'error' : 'Login failed. Please supply a valid username and password'
            }, 400)




class ObtainAccessToken(viewsets.ViewSet):
    """RefreshToken API"""
    page_name = None

    def get_view_name(self):
        return self.page_name

    @extend_schema(**AccessTokenSpecs.create)
    def create(self, request):
        """RefreshToken - POST Endpoint"""

        self.page_name = "Get Access Token"
        refresh_token = request.data.get('refresh_token', None)

        if not refresh_token:
            return Response({
                'error': 'refresh_token is required'
                }, status=400)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            access_validity = access_token.current_time + access_token.lifetime 

            if IST_TZ is not None:
                access_validity = access_validity.astimezone(IST_TZ)

            return Response({
                'access_token': str(access_token),
                'valid_upto': str(access_validity)
                }, 200)

        except Exception as excp:
            return Response({
                'error': f'Failed to refresh token: {str(excp)}'
                }, status=400)
