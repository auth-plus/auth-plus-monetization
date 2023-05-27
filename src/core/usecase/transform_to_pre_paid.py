from functools import reduce
from uuid import UUID

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.discount import Discount, DiscountType
from src.core.usecase.driven.creating_charge import CreatingCharge
from src.core.usecase.driven.creating_invoice import CreatingInvoice
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_discount import ReadingDiscount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount


class TransformToPrePaid:
    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        creating_charge: CreatingCharge,
        update_account: UpdateAccount,
        reading_discount: ReadingDiscount,
        reading_account: ReadingAccount,
        creating_invoice: CreatingInvoice,
    ):
        self.reading_transaction = reading_transaction
        self.creating_charge = creating_charge
        self.update_account = update_account
        self.reading_discount = reading_discount
        self.reading_account = reading_account
        self.creating_invoice = creating_invoice

    def transform_to_pre_paid(self, account_id: UUID):
        account = self.reading_account.by_id(account_id)
        if account.type is AccountType.POST_PAID:
            raise Exception("This account already is PostPaid")
        total_debit = self._calculate_total_debit(account)
        discount = self.reading_discount.by_account_id(account.id)
        amount = self._apply_discount(total_debit, discount)
        self._should_create_invoice(account.id, amount)
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
            return amount * (1 - discount.amount)

    def _should_create_invoice(self, account_id: UUID, amount: float) -> None:
        if amount < 0:
            item = InvoiceItem("PostPaid transform", -amount, "BRL", 1.0)
            invoice = self.creating_invoice.create_invoice(account_id, [item])
            self.creating_charge.create_charge(invoice.id)
        else:
            if amount > 0:
                raise Exception(
                    "PostPaid Account should not have credit, only debit or 0"
                )
