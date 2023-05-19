from functools import reduce
from uuid import UUID

from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class GetTotalCredit:
    def __init__(
        self, reading_transaction: ReadingTransaction, reading_account: ReadingAccount
    ):
        self.reading_transaction = reading_transaction
        self.reading_account = reading_account

    def get_total_credit(self, account_id: UUID) -> float:
        account = self.reading_account.by_id(account_id)
        transaction_list = self.reading_transaction.by_account_id(
            account_id, account.created_at
        )
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: a + b, amount_list)
