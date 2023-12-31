from pytest_factoryboy import register
from .factories import PurchaseOrderFactory, LineItemFactory, SupplierFactory

register(PurchaseOrderFactory)
register(LineItemFactory)
register(SupplierFactory)