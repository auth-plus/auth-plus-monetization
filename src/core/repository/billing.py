from uuid import UUID

from src.core.entity.billing import InvoiceItem
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser


class Billing(CreatingCharge, CreatingInvoice, FetchBillingUser):
    def fetch_by_account_id(self, accountId: UUID):
        pass

    def create_invoice(self, item_list: list[InvoiceItem]):
        pass

    def create_charge(self, invoice_id: UUID):
        pass
