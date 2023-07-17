from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.account import Account, AccountType
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.get_total_credit import GetTotalCredit


def test_should_charge_debit():
    account_id = uuid4()
    external_id = uuid4()
    type = AccountType.PRE_PAID
    created_at = datetime.now()
    account = Account(account_id, external_id, type, True, created_at)
    transaction1 = Transaction(
        uuid4(), account_id, 1.0, "desc", uuid4(), datetime.today()
    )
    transaction2 = Transaction(
        uuid4(), account_id, 2.0, "desc", uuid4(), datetime.today()
    )
    transaction_list = [transaction1, transaction2]
    # mock
    reading_account: ReadingAccount = AccountRepository()
    reading_account.by_id = MagicMock(return_value=account)
    reading_transaction: ReadingTransaction = LedgerRepository()
    reading_transaction.by_account_id = MagicMock(return_value=transaction_list)
    # usecase
    usecase = GetTotalCredit(reading_account, reading_transaction)
    result = usecase.get_total_credit(account_id)
    # assert
    assert result == 3.0
    reading_account.by_id.assert_called_once_with(account_id)
    reading_transaction.by_account_id.assert_called_once_with(account_id, created_at)
