from uuid import UUID
from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser


class ReceiveCredit:
    def __init__(
        self,
        fetch_billing_user: FetchBillingUser,
        creating_invoice: CreatingInvoice,
        creating_charge: CreatingCharge,
        creating_transaction: CreatingTransaction,
    ):
        self.fetch_billing_user = fetch_billing_user
        self.creating_invoice = creating_invoice
        self.creating_charge = creating_charge
        self.creating_transaction = creating_transaction

    def receive_credit(self, account_id: UUID, amount: float):
        credit = InvoiceItem("CREDIT", amount, "BRL", 1.0)
        item_list = [credit]
        billing_user = self.fetch_billing_user.fetch_by_account_id(account_id)
        invoice = self.creating_invoice.create_invoice(item_list)
        charge = self.creating_charge.create_charge(invoice)
        self.creating_transaction.create_transaction(account_id, amount)
        return charge
