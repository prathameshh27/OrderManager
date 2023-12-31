from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.auth_viewset import ObtainTokenPair, ObtainAccessToken

router = DefaultRouter()

router.register(r"token", ObtainTokenPair, basename="obtain_token_pair")
router.register(r"token/refresh", ObtainAccessToken, basename="refresh_token")


urlpatterns = [
    path('', include(router.urls), name='Token Based Auth'),
]
