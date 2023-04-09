from functools import reduce
from uuid import UUID
from src.core.entity.account import AccountType

from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.creating_transaction import CreatingTransaction
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
    ):
        self.reading_transaction = reading_transaction
        self.creating_discount = creating_discount
        self.creating_transaction = creating_transaction
        self.update_account = update_account

    def transform_to_post_paid(self, account_id: UUID):
        transaction_list = self.reading_transaction.by_account_id(account_id)
        amount_list = list(map(lambda a: a.amount, transaction_list))
        total = reduce(lambda a, b: a + b, amount_list)
        self.creating_discount.create_discount(account_id, self.reason, total)
        amount_to_reset_value = -total
        self.creating_transaction.create_transaction(account_id, amount_to_reset_value)
        self.update_account.change_type(account_id, AccountType.POST_PAID)
