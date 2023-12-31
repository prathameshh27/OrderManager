import factory

from home.models.order import PurchaseOrder, LineItem
from home.models.supplier import Supplier


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    id = "supid543"
    name = "test_supplier"
    email = "test@supplier.com"



class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    id = "poid235"
    supplier = factory.SubFactory(SupplierFactory)
    order_time = "2023-12-31T16:44:12.667116+05:30"
    order_number = 1234
    total_quantity = 5
    total_amount = "100.00"
    total_tax = "10.00"


class LineItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LineItem

    id = "liabc1"
    item_name = "SKU987"
    quantity = 5
    price_without_tax = "18.00"
    tax_name = "VAT"
    tax_amount = "2.00"
    line_total = "100.00"
    purchase_order = factory.SubFactory(PurchaseOrderFactory) 

