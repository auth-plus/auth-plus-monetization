from functools import reduce
from uuid import UUID

from src.core.entity.account import AccountType
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount


class TransformToPostPaid:
    reason = "TransformToPostPaid"

    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        creating_discount: CreatingDiscount,
        creating_transaction: CreatingTransaction,
        update_account: UpdateAccount,
        reading_account: ReadingAccount,
    ):
        self.reading_transaction = reading_transaction
        self.creating_discount = creating_discount
        self.creating_transaction = creating_transaction
        self.update_account = update_account
        self.reading_account = reading_account

    def transform_to_post_paid(self, account_id: UUID):
        total_credit = self._calculate_total_credit(account_id)
        self._should_create_discount(account_id, total_credit)
        self.update_account.change_type(account_id, AccountType.POST_PAID)

    def _calculate_total_credit(self, account_id: UUID):
        account = self.reading_account.by_id(account_id)
        transaction_list = self.reading_transaction.by_account_id(
            account_id, account.created_at
        )
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: a + b, amount_list)

    def _should_create_discount(self, account_id: UUID, amount: float):
        if amount > 0:
            self.creating_discount.create_discount(account_id, self.reason, amount)
        else:
            if amount < 0:
                raise Exception(
                    "PrePaid Account should not have debit, only credit or 0"
                )
