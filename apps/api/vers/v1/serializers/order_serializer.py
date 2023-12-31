from rest_framework import serializers
from apps.home.models.order import PurchaseOrder, LineItem
from .supplier_serializer import SupplierSerializer


class LineItemSerializer(serializers.ModelSerializer):
    """Generic Purchase Order Items Serializer"""
    class Meta:
        """Properties"""
        model = LineItem
        # exclude = ('purchase_order',)
        fields = ("id", "item_name", "quantity", "price_without_tax", "tax_name", "tax_amount", "line_total")

    id = serializers.CharField(read_only=False, required=False, allow_null=True)
    quantity = serializers.IntegerField(allow_null=False, min_value=1)
    price_without_tax = serializers.DecimalField(allow_null=False, min_value=0, max_digits=12, decimal_places=2)
    tax_amount = serializers.DecimalField(allow_null=False, min_value=0, max_digits=12, decimal_places=2)
    line_total = serializers.DecimalField(read_only=True, min_value=0, max_digits=12, decimal_places=2)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Generic Purchase Order Serializer"""

    class Meta:
        """Properties"""
        depth = 1
        model = PurchaseOrder

        # defined all the fields to retrive all the columns in a specified order as depicted in the problem statement
        fields = ('id', 'supplier', 'order_number', 'order_time', 'total_amount', 'total_quantity', 'total_tax', 'line_items')
        read_only_fields = ['order_number', 'order_time', 'total_amount', 'total_quantity', 'total_tax']

    total_tax = serializers.DecimalField(read_only=True, min_value=0, max_digits=12, decimal_places=2)
    total_amount = serializers.DecimalField(read_only=True, min_value=0, max_digits=12, decimal_places=2)
    
    supplier = SupplierSerializer()
    line_items = LineItemSerializer(many=True)


    def _process_line_items(self, line_items:list, order_instance:object, method:str) -> tuple:
        """Preprocessing step for line items | Returns (order_header, updated_line_items)"""

        if not (line_items and isinstance(line_items, list) and len(line_items) > 0):
            raise serializers.ValidationError({"error_msg" : "line_items_missing - Atleast 1 line item is required"})

        line_item_instances = []
        total_amount, total_quantity, total_tax = 0,0,0

        if method=="update":
            updated_item_instances, new_items_instances = [], []
            updated_item_ids = []
            existing_items = order_instance.line_items.all()

        for indx, item in enumerate(line_items):
            item = dict(item)

            line_qty = int(item.get("quantity", 0))
            total_gross_amount = line_qty * float(item.get("price_without_tax", 0))
            total_tax_amount = line_qty * float(item.get("tax_amount", 0))
            total_line_amount = total_gross_amount + total_tax_amount

            item["line_total"] = total_line_amount
            item["purchase_order"] = order_instance

            line_items[indx] = item

            total_amount += total_line_amount
            total_quantity += line_qty
            total_tax += total_tax_amount

            if method == "create":
                _ = item.pop("id", None)
                line_item_instances.append(LineItem(**item))
            
            elif method == "update":
                item['id'] = item.get('id', None)
                if item['id']:
                    try:
                        item_instance = existing_items.get(id=item['id'])
                        item_instance.update_fields(**item)
                        updated_item_instances.append(item_instance)
                        updated_item_ids.append(item['id'])

                    except Exception:
                        raise serializers.ValidationError({"error_msg" : f"item_not_found - {item['id']} does not exist in the Purchase Order" })

                else:
                    _ = item.pop('id', None)
                    new_items_instances.append(LineItem(**item))

        if method=="update":
            existing_items.exclude(id__in = updated_item_ids).delete()
            new_items_instances = LineItem.objects.bulk_create(new_items_instances)
            line_item_instances = updated_item_instances + new_items_instances

        order_header = {
            "total_amount": total_amount, 
            "total_quantity": total_quantity, 
            "total_tax": total_tax
        }

        return order_header, line_item_instances



    def _upsert_supplier(self, supplier_data:dict) -> object:
        supplier_serializer = SupplierSerializer(data=supplier_data)
        supplier_serializer.is_valid(raise_exception=True)
        supplier = supplier_serializer.save()
        return supplier


    def create(self, validated_data) -> object:
        """Create and return a new PurchaseOrder instance."""

        line_items = validated_data.get('line_items', [])
        supplier_data = validated_data.get("supplier")

        supplier = self._upsert_supplier(supplier_data)
        order_instance = PurchaseOrder(supplier=supplier)

        order_header, line_items = self._process_line_items(line_items, order_instance, method="create")
        order_instance.update_fields(**order_header)

        order_instance.save()

        LineItem.objects.bulk_create(line_items)

        return order_instance



    def update(self, order_instance, validated_data):
        """Update and return an existing PurchaseOrder instance."""

        line_items = validated_data.get('line_items', [])
        supplier_data = validated_data.get("supplier")


        order_header, line_items = self._process_line_items(line_items, order_instance, method="update")
        order_header["supplier"] = self._upsert_supplier(supplier_data)

        order_instance.update_fields(**order_header)
        order_instance.save()

        update_fields = ('quantity', 'tax_name', 'item_name', 'tax_amount', 'line_total', 'price_without_tax')
        LineItem.objects.bulk_update(line_items,fields=update_fields)

        return order_instance
