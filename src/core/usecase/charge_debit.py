from datetime import datetime
from uuid import UUID

from src.core.entity.billing import Charge, InvoiceItem
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class ChargeDebit:
    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        creating_invoice: CreatingInvoice,
        creating_charge: CreatingCharge,
    ):
        self.reading_transaction = reading_transaction
        self.creating_invoice = creating_invoice
        self.creating_charge = creating_charge

    def charge_debit(
        self, account_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> Charge:
        transaction_list = self.reading_transaction.by_account_id(
            account_id, date_start, date_end
        )
        invoice_item_list = list(
            map(
                lambda tran: InvoiceItem(tran.description, tran.amount, "BRL", 1.0),
                transaction_list,
            )
        )
        invoice = self.creating_invoice.create_invoice(account_id, invoice_item_list)
        charge = self.creating_charge.create_charge(invoice.id)
        return charge
