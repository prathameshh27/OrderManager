from django.contrib import admin

from .models.order import PurchaseOrder, LineItem
from .models.supplier import Supplier
from .models.document_counter import DocumentCounter

class AdminSupplier(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']

class AdminPurchaseOrder(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'order_time', 'order_number', 'total_quantity', 'total_amount']

class AdminLineItem(admin.ModelAdmin):
    list_display = ['id', 'purchase_order', 'item_name', 'quantity', 'price_without_tax', 'tax_name', 'tax_amount', 'line_total']

class AdminDocumentCounter(admin.ModelAdmin):
    list_display = ['document_type', 'document_number']

# Register your models here.
admin.site.register(Supplier, AdminSupplier)
admin.site.register(PurchaseOrder, AdminPurchaseOrder)
admin.site.register(LineItem, AdminLineItem)
admin.site.register(DocumentCounter, AdminDocumentCounter)