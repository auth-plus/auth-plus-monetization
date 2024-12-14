from uuid import UUID

from src.core.entity.account import AccountType
from src.core.entity.billing import InvoiceItem
from src.core.helpers import FlowPrePaidError
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount


class ReceiveCredit:
    """
    This class should only be used by pre-paid type of plan
    when the user wants to add credit in their account
    """

    def __init__(
        self,
        reading_account: ReadingAccount,
        billing_fetch_user: BillingFetchUser,
        billing_updating_invoice: BillingUpdatingInvoice,
        creating_transaction: CreatingTransaction,
    ):
        self.reading_account = reading_account
        self.billing_fetch_user = billing_fetch_user
        self.billing_updating_invoice = billing_updating_invoice
        self.creating_transaction = creating_transaction

    def receive_credit(self, external_id: UUID, amount: float):
        account = self.reading_account.by_external_id(external_id)
        if account.type is AccountType.POST_PAID:
            raise FlowPrePaidError()
        credit = InvoiceItem("CREDIT", amount, "BRL", 1.0)
        item_list = [credit]
        self.billing_fetch_user.fetch_by_account_id(external_id)
        invoice = self.billing_updating_invoice.add_item(external_id, item_list)
        self.billing_updating_invoice.charge(invoice.id)
        transaction = self.creating_transaction.create_transaction(
            account.id, amount, "credit receive", None
        )
        return transaction
