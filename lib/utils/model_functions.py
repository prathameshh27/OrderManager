import uuid
from django.db import transaction

# Used for replacing the default sequential IDs in the models
def custom_id():
    """generates 8 character alphanumeric ID"""
    unique_id = str(uuid.uuid4())[:8]
    return unique_id


def set_doc_number(doc_type):
    """Get the new incremental number for the document. Allowed doc_type: ORDER|INVOICE"""
    
    # atomic transaction will roll back if the transaction fails in the middle
    with transaction.atomic():
        from apps.home.models.document_counter import DocumentCounter
        row = DocumentCounter.objects.select_for_update(nowait=False).filter(document_type=doc_type)
        if row:
            row = row[0]
            row.document_number += 1
            row.save()
        else:
            row = DocumentCounter.objects.select_for_update(nowait=False).create(document_type=doc_type)
        return row.document_number