from functools import reduce
from uuid import UUID

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.discount import Discount, DiscountType
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount


class TransformToPrePaid:
    def __init__(
        self,
        reading_account: ReadingAccount,
        reading_transaction: ReadingTransaction,
        reading_discount: ReadingDiscount,
        billing_charge_debit: BillingCharge,
        update_account: UpdateAccount,
    ):
        self.reading_account = reading_account
        self.reading_transaction = reading_transaction
        self.reading_discount = reading_discount
        self.billing_charge_debit = billing_charge_debit
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
            item = InvoiceItem("PostPaid transform", -amount, "BRL", 1.0)
            self.billing_charge_debit.charge(external_id, [item])
        else:
            if amount > 0:
                raise SystemError(
                    "PostPaid Account should not have credit, only debit or 0"
                )
