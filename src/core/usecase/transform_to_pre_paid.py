from functools import reduce
from uuid import UUID

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.discount import Discount, DiscountType
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdatingAccount


class TransformToPrePaid:
    """
    This class should only be used by post-paid type of plan
    when the user wish to switch plan
    """

    def __init__(
        self,
        reading_account: ReadingAccount,
        reading_transaction: ReadingTransaction,
        reading_discount: ReadingDiscount,
        billing_updating_invoice: BillingUpdatingInvoice,
        update_account: UpdatingAccount,
    ):
        self.reading_account = reading_account
        self.reading_transaction = reading_transaction
        self.reading_discount = reading_discount
        self.billing_updating_invoice = billing_updating_invoice
        self.update_account = update_account

    def transform_to_pre_paid(self, external_id: UUID):
        account = self.reading_account.by_external_id(external_id)
        if account.type is AccountType.POST_PAID:
            raise SystemError("This account already is PostPaid")
        total_debit = self._calculate_total_debit(account)
        discount = self.reading_discount.by_account_id(account.id)
        amount = self._apply_discount(total_debit, discount)
        self._charge_debit(external_id, amount)
        self.update_account.change_type(account.id, AccountType.PRE_PAID)

    def _calculate_total_debit(self, account: Account):
        transaction_list = self.reading_transaction.by_account_id(
            account.id, account.created_at
        )
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: a + b, amount_list)

    def _apply_discount(self, amount: float, discount: Discount) -> float:
        if discount.type is DiscountType.ABSOLUTE:
            return amount - discount.amount
        else:
            return amount * (100 - discount.amount) / 100

    def _charge_debit(self, external_id: UUID, amount: float) -> None:
        if amount < 0:
            item = InvoiceItem("PostPaid transform", amount, "BRL", 1.0)
            invoice = self.billing_updating_invoice.add_item(external_id, [item])
            self.billing_updating_invoice.charge(invoice.id)
        else:
            if amount > 0:
                raise ValueError(
                    "PostPaid Account should not have credit, only debit or 0"
                )
