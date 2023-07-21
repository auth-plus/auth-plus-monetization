from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.transaction import Transaction
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.charge_debit import ChargeDebit
from src.core.usecase.driven.billing.billing_charge import BillingCharge
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_transaction import ReadingTransaction


def test_should_charge_debit(session: Session):
    account_id = uuid4()
    external_id = uuid4()
    account = Account(
        account_id, external_id, AccountType.PRE_PAID, True, datetime.now()
    )
    date_start = datetime.today() - timedelta(days=1)
    date_end = datetime.now()
    transaction = Transaction(
        uuid4(), account_id, 1.0, "desc", uuid4(), datetime.today()
    )
    transaction_list = [transaction]
    invoice_item_list = list(
        map(
            lambda transac: InvoiceItem(
                transac.description, transac.amount, "BRL", 1.0
            ),
            transaction_list,
        )
    )
    # mock
    reading_account: ReadingAccount = LedgerRepository(session)
    reading_account.by_external_id = MagicMock(return_value=account)
    reading_transaction: ReadingTransaction = LedgerRepository(session)
    reading_transaction.by_account_id = MagicMock(return_value=transaction_list)
    billing_charge: BillingCharge = LedgerRepository(session)
    billing_charge.charge = MagicMock(return_value=None)
    # usecase
    usecase = ChargeDebit(reading_account, reading_transaction, billing_charge)
    usecase.charge_debit(external_id, date_start, date_end)
    # assert
    reading_account.by_external_id.assert_called_once_with(external_id)
    reading_transaction.by_account_id.assert_called_once_with(
        account_id, date_start, date_end
    )
    billing_charge.charge.assert_called_once_with(external_id, invoice_item_list)
