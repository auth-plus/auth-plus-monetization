from uuid import UUID
from src.core.entity.account import AccountType
from src.core.usecase.driven.creating_charge import CreatingCharge

from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount


class TransformToPrePaid:
    def __init__(
        self,
        reading_transaction: ReadingTransaction,
        creating_charge: CreatingCharge,
        update_account: UpdateAccount,
    ):
        self.reading_transaction = reading_transaction
        self.creating_charge = creating_charge
        self.update_account = update_account

    def transform_to_pre_paid(self, account_id: UUID):
        transaction = self.reading_transaction.get_last_transaction(account_id)
        self.creating_charge.create_charge(transaction.invoice_id)
        self.update_account.change_type(account_id, AccountType.PRE_PAID)
