from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.account import Account, AccountType
from src.core.entity.discount import DiscountType
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.discount import DiscountRepository
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_account import UpdateAccount
from src.core.usecase.transform_to_post_paid import TransformToPostPaid


def test_should_transform_to_post_paid():
    account_id = uuid4()
    external_id = uuid4()
    account_created_at = datetime.now()
    account = Account(
        account_id, external_id, AccountType.PRE_PAID, True, account_created_at
    )
    transaction_id = uuid4()
    transaction_1 = Transaction(
        transaction_id, account_id, 1.0, "descrip", uuid4(), datetime.today()
    )
    transaction_2 = Transaction(
        transaction_id, account_id, 2.0, "descrip", uuid4(), datetime.today()
    )
    transaction_3 = Transaction(
        transaction_id, account_id, 3.0, "descrip", uuid4(), datetime.today()
    )
    # mock
    reading_account: ReadingAccount = AccountRepository()
    reading_account.by_external_id = MagicMock(return_value=account)
    reading_transaction: ReadingTransaction = LedgerRepository()
    reading_transaction.by_account_id = MagicMock(
        return_value=[transaction_1, transaction_2, transaction_3]
    )
    creating_discount: CreatingDiscount = DiscountRepository()
    creating_discount.create_discount = MagicMock(return_value=None)
    update_account: UpdateAccount = AccountRepository()
    update_account.change_type = MagicMock(return_value=None)
    # usecase
    usecase = TransformToPostPaid(
        reading_account,
        reading_transaction,
        creating_discount,
        update_account,
    )
    usecase.transform_to_post_paid(external_id)
    # assert
    reading_account.by_external_id.assert_called_once_with(external_id)
    reading_transaction.by_account_id.assert_called_once_with(
        account_id, account_created_at
    )
    creating_discount.create_discount.assert_called_once_with(
        account_id, "TransformToPostPaid", 6.0, DiscountType.ABSOLUTE
    )
    update_account.change_type.assert_called_once_with(
        account_id, AccountType.POST_PAID
    )
