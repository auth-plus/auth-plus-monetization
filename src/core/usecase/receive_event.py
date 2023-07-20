from uuid import UUID

from src.core.entity.event import convert_str_to_event_type
from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_event import ReadingEvent


class ReceiveEvent:
    def __init__(
        self,
        reading_event: ReadingEvent,
        reading_account: ReadingAccount,
        creating_transaction: CreatingTransaction,
    ):
        self.reading_event = reading_event
        self.reading_account = reading_account
        self.creating_transaction = creating_transaction

    def receive_event(self, external_id: UUID, event_input: str) -> Transaction:
        event_type = convert_str_to_event_type(event_input)
        event = self.reading_event.by_type(event_type)
        debit = -event.value
        account = self.reading_account.by_external_id(external_id)
        transaction = self.creating_transaction.create_transaction(
            account.id, debit, "event receive", event.id
        )
        return transaction
