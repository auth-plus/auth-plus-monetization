from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.billing import InvoiceItem
from src.core.entity.event import Event, EventType
from src.core.entity.transaction import Transaction
from src.core.repository.account import AccountRepository
from src.core.repository.billing import BillingService
from src.core.repository.ledger import LedgerRepository
from src.core.repository.price import PriceRepository
from src.core.usecase.driven.billing.billing_updating_invoice import (
    BillingUpdatingInvoice,
)
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.reading_event import ReadingEvent
from src.core.usecase.receive_event import ReceiveEvent


def test_should_receive_event(session: Session):
    account_id = uuid4()
    external_id = uuid4()
    account = Account(
        account_id, external_id, AccountType.POST_PAID, datetime.now(), None
    )
    event_id = uuid4()
    amount = 123.4
    event_type = EventType.PHONE_AUTH_FACTOR_SENT
    event = Event(event_id, event_type, amount, datetime.now())
    transaction_id = uuid4()
    transaction = Transaction(
        transaction_id, account_id, -amount, "descrip", event_id, datetime.today()
    )
    # mock
    reading_event: ReadingEvent = PriceRepository(session)
    reading_event.by_event = MagicMock(return_value=event)
    reading_account: ReadingAccount = AccountRepository(session)
    reading_account.by_external_id = MagicMock(return_value=account)
    creating_transaction: CreatingTransaction = LedgerRepository(session)
    creating_transaction.create_transaction = MagicMock(return_value=transaction)
    billing_updating_invoice: BillingUpdatingInvoice = BillingService()
    billing_updating_invoice.add_item = MagicMock(return_value=None)
    # usecase
    usecase = ReceiveEvent(
        reading_event, reading_account, creating_transaction, billing_updating_invoice
    )
    result = usecase.receive_event(external_id, "PHONE_AUTH_FACTOR_SENT")
    # assert
    assert result.id == transaction_id
    assert result.account_id == account_id
    assert result.amount == -amount
    assert result.event_id == event_id
    reading_event.by_event.assert_called_once_with(event_type)
    reading_account.by_external_id.assert_called_once_with(external_id)
    creating_transaction.create_transaction.assert_called_once_with(
        account_id, -amount, "event receive", event_id
    )
    billing_updating_invoice.add_item.assert_called_once_with(
        external_id, [InvoiceItem(str(event.type), event.price, "BRL", 1)]
    )
