from functools import reduce
from uuid import UUID
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class GetTotalCredit:
    def __init__(self, reading_transaction: ReadingTransaction):
        self.reading_transaction = reading_transaction

    def get_total_credit(self, account_id: UUID) -> float:
        transaction_list = self.reading_transaction.by_account_id(account_id)
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: a + b, amount_list)
