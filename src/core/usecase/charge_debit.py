from datetime import datetime
from uuid import UUID

from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class ChargeDebit:
    def __init__(
        self,
        reading_account: ReadingAccount,
        reading_transaction: ReadingTransaction,
        billing_charge: BillingCharge,
    ):
        self.reading_account = reading_account
        self.reading_transaction = reading_transaction
        self.billing_charge = billing_charge

    def charge_debit(
        self, external_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> None:
        account = self.reading_account.by_external_id(external_id)
        transaction_list = self.reading_transaction.by_account_id(
            account.id, date_start, date_end
        )
        invoice_item_list = list(
            map(
                lambda tran: InvoiceItem(tran.description, tran.amount, "BRL", 1.0),
                transaction_list,
            )
        )
        self.billing_charge.charge(external_id, invoice_item_list)
        return None
