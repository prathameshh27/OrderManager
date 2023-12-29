from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated #, IsAdminUser, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers.order_serializer import PurchaseOrderSerializer
from apps.home.models.order import PurchaseOrder


class OrderViewSet(viewsets.ViewSet):
    """Purchase Order API"""
    page_name = None

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_view_name(self):
        return self.page_name


    def create(self, request):
        """Orders - POST Endpoint"""

        self.page_name = "Create Purchase Order"

        post_data = request.data

        if not isinstance(post_data, dict):
            return Response({"error": "Invalid request body"}, 400)

        purchase_order_serializer = PurchaseOrderSerializer(data=post_data, many=False)
        purchase_order_serializer.is_valid(raise_exception=True)
        purchase_order_serializer.save()

        return Response(purchase_order_serializer.data, 200)


    def list(self, request):
        """Get All Purchase Orders"""
        self.page_name = "Get All Purchase Orders"
        
        orders = PurchaseOrder.get_all_orders(request.GET)
        order_serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(order_serializer.data)
    

    def retrieve(self, request, pk=None):
        """Get Purchase Order"""
        self.page_name = "Get Purchase Order"
        order = PurchaseOrder.get_order(id=pk)
        order_serializer = PurchaseOrderSerializer(order, many=False)
        return Response(order_serializer.data)
    

    def update(self, request, pk=None):
        """Orders - PUT Endpoint for updating a Purchase Order"""

        self.page_name = "Update Purchase Order"

        update_data = request.data

        if not isinstance(update_data, dict):
            return Response({"error": "Invalid request body"}, status=400)

        order_instance = PurchaseOrder.get_order(id=pk)
        
        if not order_instance:
            return Response({"error": "Purchase Order not found"}, status=400)


        purchase_order_serializer = PurchaseOrderSerializer(instance=order_instance, data=update_data, partial=True)
        purchase_order_serializer.is_valid(raise_exception=True)
        purchase_order_serializer.save()

        return Response(purchase_order_serializer.data, status=200)


    def destroy(self, request, pk=None):
        """Orders - DELETE Endpoint for deleting a Purchase Order"""

        self.page_name = "Delete Purchase Order"

        order_instance = PurchaseOrder.get_order(id=pk)

        if not order_instance:
            return Response({"error": "Purchase Order not found"}, status=404)

        order_instance.delete()

        return Response({"message": "Purchase Order deleted"}, status=200)