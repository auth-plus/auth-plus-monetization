from uuid import UUID

from src.core.entity.event import convert_str_to_event_type
from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_event import ReadingEvent


class ReceiveEvent:
    def __init__(
        self,
        creating_transaction: CreatingTransaction,
        reading_event: ReadingEvent,
    ):
        self.creating_transaction = creating_transaction
        self.reading_event = reading_event

    def receive_event(self, account_id: UUID, event_input: str) -> Transaction:
        event_type = convert_str_to_event_type(event_input)
        event = self.reading_event.by_type(event_type)
        debit = -event.value
        transaction = self.creating_transaction.create_transaction(account_id, debit)
        return transaction
