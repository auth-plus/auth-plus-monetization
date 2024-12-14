from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import AccountType
from src.core.repository.ledger import LedgerRepository
from tests.factory.helpers import (
    create_account,
    create_transaction,
    delete_account,
    delete_transaction,
    get_event,
)


def test_should_create_transaction(session: Session):
    amount = 123.4
    description = "descript"
    event = get_event(session)
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    repository = LedgerRepository(session)
    result = repository.create_transaction(account.id, amount, description, event.id)
    assert isinstance(result.id, UUID)
    assert result.account_id == account.id
    assert result.amount == amount
    assert result.description == description
    assert result.event_id == event.id
    assert isinstance(result.created_at, datetime)
    delete_transaction(session, result.id)
    delete_account(session, account.id)


def test_should_select_by_account_id(session: Session):
    event = get_event(session)
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    transaction = create_transaction(session, account.id, 123.4, "descript", event.id)
    repository = LedgerRepository(session)
    result = repository.by_account_id(account.id, datetime.now())
    assert len(result) == 1
    assert isinstance(result[0].id, UUID)
    assert result[0].account_id == account.id
    assert result[0].amount == transaction.amount
    assert result[0].description == transaction.description
    assert result[0].event_id == event.id
    assert isinstance(result[0].created_at, datetime)
    delete_transaction(session, result[0].id)
    delete_account(session, account.id)
