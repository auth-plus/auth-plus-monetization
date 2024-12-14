from uuid import UUID

from src.core.entity.account import AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.event import convert_str_to_event_type
from src.core.entity.transaction import Transaction
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_event import ReadingEvent


class ReceiveEvent:
    """
    This class is used by both type of plans when the user trigger an event.
    There is two kind of flows
    Pre-paid: create the event, debit on ledger the amount
    Post-paid: create the event, debit on ledger the amount, charge on billing-service
    """

    def __init__(
        self,
        reading_event: ReadingEvent,
        reading_account: ReadingAccount,
        creating_transaction: CreatingTransaction,
        billing_updating_invoice: BillingUpdatingInvoice,
    ):
        self.reading_event = reading_event
        self.reading_account = reading_account
        self.creating_transaction = creating_transaction
        self.billing_updating_invoice = billing_updating_invoice

    def receive_event(self, external_id: UUID, event_input: str) -> Transaction:
        event_type = convert_str_to_event_type(event_input)
        event = self.reading_event.by_event(event_type)
        debit = -event.price
        account = self.reading_account.by_external_id(external_id)
        transaction = self.creating_transaction.create_transaction(
            account.id, debit, "event receive", event.id
        )
        if account.type is AccountType.POST_PAID:
            item_list = [InvoiceItem(str(event.type), event.price, "BRL", 1)]
            self.billing_updating_invoice.add_item(external_id, item_list)
        return transaction
