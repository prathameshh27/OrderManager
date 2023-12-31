import pytest

pytestmark = pytest.mark.django_db


class TestSupplierModel:
    def test_str_method(self, supplier_factory):
        supplier = supplier_factory()
        assert supplier.__str__() == "test_supplier"


class TestPurchaseOrderModel:
    def test_str_method(self, purchase_order_factory):
        purchase_order = purchase_order_factory()
        assert purchase_order.__str__() == "PO#1234"


# class TestLineItemModel:
#     def test_str_method(self, line_item_factory):
#         line_item = line_item_factory()
#         assert line_item.__str__() == "PO#1234 - LineItem: liabc1, Item: SKU987"


