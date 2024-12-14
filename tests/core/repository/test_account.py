from copy import deepcopy
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.entity.account import AccountType
from src.core.repository.account import AccountRepository, account_table
from tests.factory.helpers import create_account, delete_account


def test_should_create(session: Session):
    external_id = uuid4()
    type_ = AccountType.PRE_PAID

    repository = AccountRepository(session)
    result = repository.create(external_id, type_)
    assert isinstance(result.id, UUID)
    assert result.external_id == external_id
    assert result.type == type_
    assert result.deleted_at is None
    assert isinstance(result.created_at, datetime)
    delete_account(session, result.id)


def test_should_select_by_id(session: Session):
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    repository = AccountRepository(session)
    result = repository.by_id(account.id)
    assert result.id == account.id
    assert result.external_id == account.external_id
    assert result.type == account.type
    assert result.deleted_at is None
    assert result.created_at == account.created_at
    delete_account(session, account.id)


def test_should_select_by_external_id(session: Session):
    external_id = uuid4()
    account = create_account(session, external_id, AccountType.POST_PAID)
    repository = AccountRepository(session)
    result = repository.by_external_id(external_id)
    assert result.id == account.id
    assert result.external_id == account.external_id
    assert result.type == account.type
    assert result.deleted_at is None
    assert result.created_at == account.created_at
    delete_account(session, account.id)


def test_should_update_type(session: Session):
    external_id = uuid4()
    account = create_account(session, external_id, AccountType.PRE_PAID)
    repository = AccountRepository(session)
    repository.change_type(account.id, AccountType.POST_PAID)
    select_query = (
        select(account_table).where(account_table.c.id == account.id).limit(1)
    )
    cursor = session.execute(select_query).first()
    if cursor is None:
        raise SystemError("test: test_should_update_type something went wrong")
    result = deepcopy(cursor)
    assert result[0] == account.id
    assert result[1] == account.external_id
    assert result[2] == AccountType.POST_PAID
    assert result[3] == account.created_at
    assert result[4] is None
    delete_account(session, account.id)
