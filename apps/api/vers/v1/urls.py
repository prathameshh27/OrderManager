from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.order_viewset import OrderViewSet


router = DefaultRouter()

router.register(r"purchase/order", OrderViewSet, basename="purchase_order")




urlpatterns = [
    path('', include(router.urls)),
]
