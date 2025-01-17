from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import Charge, Invoice
from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.ledger import LedgerRepository
from src.core.usecase.charge_debit import ChargeDebit
from src.core.usecase.driven.billing.billing_fetching_invoice import (
    BillingFetchingInvoice,
)
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.update_transaction import UpdatingTransaction


def test_should_charge_debit(session: Session):
    account_id = uuid4()
    external_id = uuid4()
    account = Account(
        account_id, external_id, AccountType.POST_PAID, datetime.now(), None
    )
    invoice = Invoice(uuid4(), external_id, "Draft", datetime.today())
    charge = Charge(uuid4(), invoice.id, "Pending", uuid4())
    # mock
    reading_account: ReadingAccount = AccountRepository(session)
    reading_account.by_subscription_period = MagicMock(return_value=[account])
    billing_fetching_invoice: BillingFetchingInvoice = BillingService()
    billing_fetching_invoice.get_current = MagicMock(return_value=invoice)
    billing_updating_invoice: BillingUpdatingInvoice = BillingService()
    billing_updating_invoice.charge = MagicMock(return_value=charge)
    updating_transaction: UpdatingTransaction = LedgerRepository(session)
    updating_transaction.add_charge = MagicMock(return_value=None)
    # usecase
    usecase = ChargeDebit(
        reading_account,
        billing_updating_invoice,
        billing_fetching_invoice,
        updating_transaction,
    )
    usecase.charge_debit()
    # assert
    reading_account.by_subscription_period.assert_called_once()
    billing_fetching_invoice.get_current.assert_called_once_with(external_id)
    billing_updating_invoice.charge.assert_called_once_with(invoice.id)
    updating_transaction.add_charge.assert_called_once_with(account_id, charge.id)
