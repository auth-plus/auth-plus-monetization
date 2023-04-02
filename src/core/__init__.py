from src.core.repository.billing import Billing
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.fetch_billing_user import FetchBillingUser
from src.core.usecase.pre_paid.receive_credit import ReceiveCredit


class Core:
    @staticmethod
    def get_instance():
        fetch_billing_user: FetchBillingUser = Billing()
        creating_invoice: CreatingInvoice = Billing()
        creating_charge: CreatingCharge = Billing()
        creating_transaction: CreatingTransaction = Billing()

        receive_credit = ReceiveCredit(
            fetch_billing_user, creating_invoice, creating_charge, creating_transaction
        )

        pre_paid = {receive_credit}
        return {pre_paid}
