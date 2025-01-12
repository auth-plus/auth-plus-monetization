from src.core.entity.account import Account, AccountType
from src.core.helpers import InvoicePostPaidError
from src.core.usecase.driven.billing.billing_fetching_invoice import (
    BillingFetchingInvoice,
)
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.reading_account import ReadingAccount


class ChargeDebit:
    """
    This class should only be used by post-paid type of plan
    when the user must pay on final period subscription
    """

    def __init__(
        self,
        reading_account: ReadingAccount,
        billing_updating_invoice: BillingUpdatingInvoice,
        billing_fetching_invoice: BillingFetchingInvoice,
    ):
        self.reading_account = reading_account
        self.billing_updating_invoice = billing_updating_invoice
        self.billing_fetching_invoice = billing_fetching_invoice

    def charge_debit(self):
        user_list = self.reading_account.by_subscription_period()
        for user in user_list:
            self._charge_single_user(user)

    def _charge_single_user(self, user: Account) -> None:
        if user.type is AccountType.PRE_PAID:
            return
        current_invoice = self.billing_fetching_invoice.get_current(user.external_id)
        if current_invoice.status != "draft":
            raise InvoicePostPaidError()
        self.billing_updating_invoice.charge(current_invoice.id)
        return None
