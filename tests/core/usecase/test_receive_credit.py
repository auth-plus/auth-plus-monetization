from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import Invoice, InvoiceItem
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.driven.billing.billing_fetch_user import BillingFetchUser
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.receive_credit import ReceiveCredit


def test_should_receive_credit(session: Session):
    account_id = uuid4()
    external_id = uuid4()
    amount = 100.99
    account = Account(
        account_id, external_id, AccountType.PRE_PAID, datetime.now(), None
    )
    transaction_id = uuid4()
    transaction = Transaction(
        transaction_id, account_id, 1.0, "desc", uuid4(), datetime.today()
    )
    invoice = Invoice(uuid4(), external_id, "draft", datetime.today())

    # mock
    reading_account: ReadingAccount = AccountRepository(session)
    reading_account.by_external_id = MagicMock(return_value=account)
    fetch_billing_user: BillingFetchUser = BillingService()
    fetch_billing_user.fetch_by_account_id = MagicMock(return_value=account)
    billing_updating_invoice: BillingUpdatingInvoice = BillingService()
    billing_updating_invoice.add_item = MagicMock(return_value=invoice)
    billing_updating_invoice.charge = MagicMock(return_value=None)
    creating_transaction: CreatingTransaction = LedgerRepository(session)
    creating_transaction.create_transaction = MagicMock(return_value=transaction)
    # usecase
    usecase = ReceiveCredit(
        reading_account,
        fetch_billing_user,
        billing_updating_invoice,
        creating_transaction,
    )
    result = usecase.receive_credit(external_id, amount)
    # assert
    assert result.id == transaction_id
    assert result.account_id == account_id
    assert result.amount == 1.0
    assert result.description == "desc"
    reading_account.by_external_id.assert_called_once_with(external_id)
    fetch_billing_user.fetch_by_account_id.assert_called_once_with(external_id)
    billing_updating_invoice.add_item.assert_called_once_with(
        external_id, [InvoiceItem("CREDIT", amount, "BRL", 1.0)]
    )
    billing_updating_invoice.charge.assert_called_once_with(invoice.id)
    creating_transaction.create_transaction.assert_called_once_with(
        account_id, amount, "credit receive", None
    )
