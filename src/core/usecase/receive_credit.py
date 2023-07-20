from uuid import UUID

from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount


class ReceiveCredit:
    def __init__(
        self,
        reading_account: ReadingAccount,
        billing_fetch_user: BillingFetchUser,
        billing_charge: BillingCharge,
        creating_transaction: CreatingTransaction,
    ):
        self.reading_account = reading_account
        self.billing_fetch_user = billing_fetch_user
        self.billing_charge = billing_charge
        self.creating_transaction = creating_transaction

    def receive_credit(self, external_id: UUID, amount: float):
        account = self.reading_account.by_external_id(external_id)
        credit = InvoiceItem("CREDIT", amount, "BRL", 1.0)
        item_list = [credit]
        self.billing_fetch_user.fetch_by_account_id(external_id)
        self.billing_charge.charge(external_id, item_list)
        transaction = self.creating_transaction.create_transaction(
            account.id, amount, "credit receive", None
        )
        return transaction
