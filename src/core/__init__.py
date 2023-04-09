from dataclasses import dataclass

from src.core.repository.billing import Billing
from src.core.repository.ledger import Ledger
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser
from src.core.usecase.pre_paid.receive_credit import ReceiveCredit


class Core:
    def __init__(self):
        fetch_billing_user: FetchBillingUser = Billing()
        creating_invoice: CreatingInvoice = Billing()
        creating_charge: CreatingCharge = Billing()
        creating_transaction: CreatingTransaction = Ledger()

        receive_credit = ReceiveCredit(
            fetch_billing_user, creating_invoice, creating_charge, creating_transaction
        )

        @dataclass
        class PrePaid:
            receive_credit: ReceiveCredit

        self.pre_paid = PrePaid(receive_credit)
