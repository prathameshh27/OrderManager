from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from ..serializers.order_serializer import PurchaseOrderSerializer
from apps.home.models.order import PurchaseOrder


class OrderSpecs:
    """OpenAPI specifications for the Purchase order API endpoints"""
    create = {
        "request": PurchaseOrderSerializer, 
        "responses": PurchaseOrderSerializer,
        "description": """<h2>Create Order</h2>
                        Allows the user to create a new purchase order.
                        Accepts multiple line items and a non existing Supplier.<br>
                        - If you are sending a non nullid in the supplier data then 
                        an existing supplier with that id is linked with the purchase order. 
                        The supplier name and email are updated based on the new data.<br>
                        - If you are sending the supplier data without an id or if the id is null 
                        then a new supplier will be created with the name and email values.""",
    }

    list_ = {
        "request": None, 
        "responses": PurchaseOrderSerializer,
        "parameters": [
            OpenApiParameter(name="supplier_name", type=str, required=False, description="filter by supplier name"),
            OpenApiParameter(name="item_name", type=str, required=False, description="filter by item name"),
        ],
        "description": """<h2>List all Purchase Orders</h2>
                        Allows the user to retrive all existing purchase orders along with the line items.
                        The orders are sorted by the PO number in descending order.<br>
                        The user can also use the query parameters to filter the list""",
    }

    retrieve = {
        "request": None, 
        "responses": PurchaseOrderSerializer,
        "parameters": [
            OpenApiParameter(name="id", type=str, location=OpenApiParameter.PATH)
            ],
        "description": """<h2>Get Purchase Order</h2>
                        Allows the user to retrive an existing purchase order with purchase order ID.
                        The response would be a dictionary with header, supplier and line item details.
                        """,
    }

    update = {
        "request": PurchaseOrderSerializer, 
        "responses": PurchaseOrderSerializer,
        "parameters": [
            OpenApiParameter(name="id", type=str, location=OpenApiParameter.PATH)
            ],
        "description": """<h2>Update Order</h2>
                        Allows the user to update an existing purchase order.
                        Accepts multiple line items and a non existing Supplier.<br>
                        - If you are sending a non nullid in the supplier data then 
                        an existing supplier with that id is linked with the purchase order. 
                        The supplier name and email are updated based on the new data.<br>
                        - If you are sending the supplier data without an id or if the id is null 
                        then a new supplier will be created with the name and email values.<br>
                        - Line items field cannot be null or an empty array.<br>
                        - If there is an id present in the line item data then the line item is 
                        updated with the new data.<br>
                        - If the id is null then a new line item is created.<br>
                        - If any line item id which was in the purchase order earlier is now 
                        absent then that line item is deleted""",
    }

    destroy = {
        "request": None, 
        "responses": None,
        "parameters": [
            OpenApiParameter(name="id", type=str, location=OpenApiParameter.PATH)
            ],
        "description": """<h2>Delete Purchase Order</h2>
                        Allows the user to delete an existing purchase order with purchase order ID.<br><br>
                        <b>response:</b> {"message": "Purchase Order deleted"}
                        """,
    }




class OrderViewSet(viewsets.ViewSet):
    """Purchase Order API"""
    page_name = None

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_view_name(self):
        return self.page_name

    

    @extend_schema(**OrderSpecs.create)
    def create(self, request):
        """Orders - POST Endpoint"""

        self.page_name = "Create Purchase Order"

        post_data = request.data

        if not isinstance(post_data, dict):
            return Response({"error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

        purchase_order_serializer = PurchaseOrderSerializer(data=post_data, many=False)
        purchase_order_serializer.is_valid(raise_exception=True)
        purchase_order_serializer.save()

        return Response(purchase_order_serializer.data, status=status.HTTP_201_CREATED)



    @extend_schema(**OrderSpecs.list_)
    def list(self, request):
        """Get All Purchase Orders"""
        self.page_name = "Get All Purchase Orders"
        
        orders = PurchaseOrder.get_all_orders(request.GET)
        order_serializer = PurchaseOrderSerializer(orders, many=True)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    


    @extend_schema(**OrderSpecs.retrieve)
    def retrieve(self, request, pk:str=None):
        """Get Purchase Order"""

        self.page_name = "Get Purchase Order"
        order_instance = PurchaseOrder.get_order(id=pk)
        
        if not order_instance:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        order_serializer = PurchaseOrderSerializer(order_instance, many=False)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    


    @extend_schema(**OrderSpecs.update)
    def update(self, request, pk=None):
        """Orders - PUT Endpoint for updating a Purchase Order"""

        self.page_name = "Update Purchase Order"

        update_data = request.data

        if not isinstance(update_data, dict):
            return Response({"error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

        order_instance = PurchaseOrder.get_order(id=pk)
        
        if not order_instance:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)


        purchase_order_serializer = PurchaseOrderSerializer(instance=order_instance, data=update_data, partial=True)
        purchase_order_serializer.is_valid(raise_exception=True)
        purchase_order_serializer.save()

        return Response(purchase_order_serializer.data, status=status.HTTP_200_OK)



    @extend_schema(**OrderSpecs.destroy)
    def destroy(self, request, pk=None):
        """Orders - DELETE Endpoint for deleting a Purchase Order"""

        self.page_name = "Delete Purchase Order"

        order_instance = PurchaseOrder.get_order(id=pk)

        if not order_instance:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order_instance.delete()

        return Response({"message": "Purchase Order deleted"}, status=status.HTTP_200_OK)