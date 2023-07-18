from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.event import Event, EventType
from src.core.entity.transaction import Transaction
from src.core.repository.billing import BillingService
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_event import ReadingEvent
from src.core.usecase.receive_event import ReceiveEvent


def test_should_receive_event():
    account_id = uuid4()
    event_id = uuid4()
    amount = 123.4
    event_type = EventType.EMAIL_CREATED
    event = Event(event_id, event_type, amount, datetime.now())
    transaction_id = uuid4()
    transaction = Transaction(
        transaction_id, account_id, -amount, "descrip", event_id, datetime.today()
    )
    # mock
    reading_event: ReadingEvent = BillingService()
    reading_event.by_type = MagicMock(return_value=event)
    creating_transaction: CreatingTransaction = BillingService()
    creating_transaction.create_transaction = MagicMock(return_value=transaction)
    # usecase
    usecase = ReceiveEvent(reading_event, creating_transaction)
    result = usecase.receive_event(account_id, "2FA_EMAIL_CREATED")
    # assert
    assert result.id == transaction_id
    assert result.account_id == account_id
    assert result.amount == -amount
    assert result.event_id == event_id
    reading_event.by_type.assert_called_once_with(event_type)
    creating_transaction.create_transaction.assert_called_once_with(
        account_id, -amount, "event receive", event_id
    )
