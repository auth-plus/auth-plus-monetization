from uuid import UUID

from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.creating_invoice import CreatingInvoice


class ReceiveEvent:
    def __init__(self):
        pass

    def receive_event(self, account_id: UUID):
        pass
