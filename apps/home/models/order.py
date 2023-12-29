from django.db import models
from django.db.models import Q
from lib.utils.model_functions import custom_id, set_doc_number

class PurchaseOrder(models.Model):

    class Meta:
        ordering = ('-order_number',)

    id = models.CharField(primary_key=True, unique=True, editable=False, default=custom_id, max_length=11)
    supplier = models.ForeignKey(to='Supplier', null=False, related_name="related_orders", on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now=True)
    order_number = models.IntegerField(unique=True, editable=False)
    total_quantity = models.PositiveIntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, null=True, blank=True, decimal_places=3)
    total_tax = models.DecimalField(max_digits=12, null=True, blank=True, decimal_places=3)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.order_number = set_doc_number("ORDER")

        super(PurchaseOrder, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"PO#{self.order_number}"
    

    def get_id(self) -> str:
        """Get Order ID"""
        return self.id


    def get_object(self) -> object:
        """Get current object"""
        return self
    

    def update_fields(self, **kwargs):
        """Update current object. Save explicitly"""
        self.supplier = kwargs.get("supplier", self.supplier)
        self.total_tax = kwargs.get("total_tax", self.total_tax)
        self.total_amount = kwargs.get("total_amount", self.total_amount)
        self.total_quantity = kwargs.get("total_quantity", self.total_quantity)


    @classmethod
    def get_order(cls, id:str) -> object:
        """Get specific order"""
        try:
            order = cls.objects.get(id=id)
        except Exception as excp:
            order = None
        return order
    
    
    @classmethod
    def get_all_orders(cls, params = {}) -> object:
        """Get all orders"""
        supplier_name = params.get("supplier_name", "")
        item_name = params.get("item_name", "")

        order = cls.objects.filter(
            Q(supplier__name__icontains=supplier_name) & 
            Q(line_items__item_name__icontains=item_name)
            )
        return order




    
class LineItem(models.Model):

    class Meta:
        ordering = ('purchase_order',)

    id = models.CharField(primary_key=True, unique=True, editable=False, default=custom_id, max_length=11)
    item_name = models.CharField(blank=False, null=False, max_length=128)
    quantity = models.PositiveIntegerField(default=1)
    price_without_tax = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    tax_name = models.CharField(max_length=32)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="line_items", on_delete=models.CASCADE)



    def save(self, *args, **kwargs):
        
        self.line_total = self.calc_line_total()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"PO#{self.purchase_order} - LineItem: {self.id}, Item: {self.item_name}"
    

    def calc_line_total(self):
        """Calculate line total"""
        return (self.quantity * self.price_without_tax) + self.tax_amount


    def update_fields(self, **kwargs):
        """Update current object. Save explicitly"""
        self.quantity = kwargs.get("quantity", self.quantity)
        self.tax_name = kwargs.get("tax_name", self.tax_name)
        self.item_name = kwargs.get("item_name", self.item_name)
        self.tax_amount = kwargs.get("tax_amount", self.tax_amount)
        self.line_total = kwargs.get("line_total", self.line_total)
        self.price_without_tax = kwargs.get("price_without_tax", self.price_without_tax)





# ++++++++++++++++++++++
# Schema: PurchaseOrder
# ++++++++++++++++++++++
# pk: int (primary key)     <= For security reason, used alpha-numeric UUID
# supplier: int (foreign key)
# order_time: datetime (auto generated)
# order_number: int (auto generated)
# total_quantity: int
# total_amount: decimal
# total_tax: decimal





# ++++++++++++++++++++++
# Schema: LineItem
# ++++++++++++++++++++++
# pk: int (primary key)     <= For security reason, used alpha-numeric UUID
# item_name: string
# quantity: int (greater than 0)
# price_without_tax: decimal (greater or equal to 0)
# tax_name: string
# tax_amount: decimal (greater or equal to 0)
# line_total: decimal (greater or equal to 0
# purchase_order: int (foreign key)