from rest_framework import serializers
from apps.home.models.supplier import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        """Properties"""
        model = Supplier
        # fields = '__all__'
        fields = ['id', 'name', 'email']

    id = serializers.CharField(read_only=False, allow_null=True)

    def create(self, validated_data):
        supplier_id = validated_data.get('id', None)

        # Check if a Supplier instance with the given id already exists
        updated_supplier, new_supplier = Supplier.objects.update_or_create(
            id=supplier_id,
            defaults=validated_data
        )

        return new_supplier if isinstance(new_supplier,Supplier) else updated_supplier