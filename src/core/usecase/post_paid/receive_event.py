from uuid import UUID

from src.core.entity.event import convert_str_to_event_type
from src.core.usecase.driven.creating_invoice_item import CreatingInvoiceItem
from src.core.usecase.driven.reading_event import ReadingEvent
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class ReceiveEvent:
    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        reading_event: ReadingEvent,
        creating_invoice_item: CreatingInvoiceItem,
    ):
        self.reading_transaction = reading_transaction
        self.reading_event = reading_event
        self.creating_invoice_item = creating_invoice_item

    def receive_event(self, account_id: UUID, event_input: str):
        event_type = convert_str_to_event_type(event_input)
        event = self.reading_event.by_type(event_type)
        transaction = self.reading_transaction.get_last_transaction(account_id)
        self.creating_invoice_item.create_invoice_item(
            transaction.invoice_id, event.type._name_, event.value, "BRL", 1.0
        )
