# ++++++++++++++++++++++
# Schema: Supplier
# ++++++++++++++++++++++
# pk: int (primary key)     <= For security reason, used alpha-numeric UUID
# name: string
# email: string

from django.db import models
from lib.utils.model_functions import custom_id


class Supplier(models.Model):
    """Supplier Model"""

    # class Meta:
    #     unique_together = 'name', 'id', 'email'

    id = models.CharField(primary_key=True, unique=True, editable=False, default=custom_id, max_length=11)
    name = models.CharField(null=False, max_length=128)
    email = models.EmailField(unique=False, null=True, blank=True, max_length=95)

    def __str__(self) -> str:
        return self.name
    

    def get_id(self) -> str:
        """Get supplier ID"""
        return self.id


    def get_object(self) -> object:
        """Get current object"""
        return self


    @classmethod
    def get_supplier(cls, id:str) -> object:
        """Get specific supplier"""
        try:
            supplier = cls.objects.get(id=id)
        except Exception as excp:
            _ = excp
            supplier = None
        return supplier
    
    
    @classmethod
    def get_all_suppliers(cls) -> object:
        """Get all suppliers"""
        supplier = cls.objects.all()
        return supplier
