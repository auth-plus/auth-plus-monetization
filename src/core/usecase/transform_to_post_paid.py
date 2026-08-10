from functools import reduce
from uuid import UUID

from src.config.logger import console
from src.core.entity.account import Account, AccountType
from src.core.entity.discount import DiscountType
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdatingAccount


class TransformToPostPaid:
    """
    This class should only be used by pre-paid type of plan
    when the user wish to switch plan
    """

    reason = "TransformToPostPaid"

    def __init__(
        self,
        reading_account: ReadingAccount,
        reading_transaction: ReadingTransaction,
        creating_discount: CreatingDiscount,
        update_account: UpdatingAccount,
    ):
        self.reading_account = reading_account
        self.reading_transaction = reading_transaction
        self.creating_discount = creating_discount
        self.update_account = update_account

    def transform_to_post_paid(self, external_id: UUID):
        console.info(f"Transforming external_id={external_id} to PostPaid")
        account = self.reading_account.by_external_id(external_id)
        if account.subscription.type is AccountType.POST_PAID_MONTH:
            console.error(f"Account {account.id} is already PostPaid")
            raise SystemError("This account already is PostPaid")
        total_credit = self._calculate_total_credit(account)
        self._should_create_discount(account.id, total_credit)
        self.update_account.change_type(account.id, AccountType.POST_PAID_MONTH)
        console.info(f"Successfully transformed account {account.id} to PostPaid")

    def _calculate_total_credit(self, account: Account) -> float:
        transaction_list = self.reading_transaction.by_account_id(
            account.id, account.created_at
        )
        amount_list = list(map(lambda a: a.amount, transaction_list))
        return reduce(lambda a, b: a + b, amount_list)

    def _should_create_discount(self, account_id: UUID, amount: float):
        if amount > 0:
            console.info(
                f"Creating discount for account {account_id} with amount {amount}"
            )
            self.creating_discount.create_discount(
                account_id, self.reason, amount, DiscountType.ABSOLUTE
            )
        else:
            if amount < 0:
                console.error(
                    f"PrePaid Account {account_id} has debit, which is not allowed"
                )
                raise ValueError(
                    "PrePaid Account should not have debit, only credit or 0"
                )
