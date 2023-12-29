from django.db import models

class DocumentCounter(models.Model):

    class DocType(models.TextChoices):
        ORDER = "ORDER"
        INVOICE = "INVOICE"

    document_type = models.CharField(choices=DocType.choices, unique=True, default=DocType.ORDER, max_length=30)
    document_number = models.IntegerField(null=True, blank=True, default=1)

    def get_id(self):
        return self.id
