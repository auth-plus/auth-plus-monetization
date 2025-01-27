from functools import reduce
from uuid import UUID

from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction


class GetTotalCredit:
    """
    This class should only be used by pre-paid type of plan
    when the user wants know their credit
    """

    def __init__(
        self,
        reading_account: ReadingAccount,
        reading_transaction: ReadingTransaction,
    ):
        self.reading_account = reading_account
        self.reading_transaction = reading_transaction

    def get_total_credit(self, external_id: UUID) -> float:
        account = self.reading_account.by_external_id(external_id)
        transaction_list = self.reading_transaction.by_account_id(
            account.id, account.created_at
        )
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: float(a + b), amount_list, 0.0)
