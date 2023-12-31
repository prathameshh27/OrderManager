from django.db import models

class DocumentCounter(models.Model):
    """Maintains a running counter for the documents"""

    class DocType(models.TextChoices):
        """Supported Documents"""

        ORDER = "ORDER"
        INVOICE = "INVOICE"

    document_type = models.CharField(choices=DocType.choices, unique=True, default=DocType.ORDER, max_length=30)
    document_number = models.IntegerField(null=True, blank=True, default=1)

    def get_id(self):
        """Get instance id"""
        return self.id
