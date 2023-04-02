from uuid import UUID
from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.creating_invoice import CreatingInvoice


class TransformToPostPaid:
    def __init__(self):
        pass

    def transform_to_post_paid(self, account: UUID):
        pass
