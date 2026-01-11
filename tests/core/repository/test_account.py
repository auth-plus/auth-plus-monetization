from copy import deepcopy
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.entity.account import AccountType
from src.core.repository.account import (
    AccountRepository,
    account_table,
    subscription_table,
)
from tests.factory.helpers import create_account, delete_account


def test_should_create(session: Session):
    external_id = uuid4()
    type_ = AccountType.PRE_PAID

    repository = AccountRepository(session)
    result = repository.create(external_id, type_)
    assert isinstance(result.id, UUID)
    assert result.external_id == external_id
    assert result.subscription.type == type_
    assert result.deleted_at is None
    assert isinstance(result.created_at, datetime)
    delete_account(session, result.id)


def test_should_select_by_id(session: Session):
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    repository = AccountRepository(session)
    result = repository.by_id(account.id)
    assert result.id == account.id
    assert result.external_id == account.external_id
    assert result.subscription.type == account.subscription.type
    assert result.deleted_at is None
    assert result.created_at == account.created_at
    delete_account(session, account.id)


def test_should_select_by_external_id(session: Session):
    external_id = uuid4()
    account = create_account(session, external_id, AccountType.POST_PAID_MONTH)
    repository = AccountRepository(session)
    result = repository.by_external_id(external_id)
    assert result.id == account.id
    assert result.external_id == account.external_id
    assert result.subscription.type == account.subscription.type
    assert result.deleted_at is None
    assert result.created_at == account.created_at
    delete_account(session, account.id)


def test_should_update_type(session: Session):
    external_id = uuid4()
    account = create_account(session, external_id, AccountType.PRE_PAID)
    repository = AccountRepository(session)
    repository.change_type(account.id, AccountType.POST_PAID_MONTH)
    select_account_query = (
        select(account_table).where(account_table.c.id == account.id).limit(1)
    )
    cursor_account = session.execute(select_account_query).first()
    if cursor_account is None:
        raise SystemError("test: test_should_update_type something went wrong")
    result_user = deepcopy(cursor_account)
    select_subscription_query = (
        select(subscription_table)
        .where(
            subscription_table.c.account_id == account.id,
            subscription_table.c.deleted_at.is_(None),
        )
        .limit(1)
    )
    cursor_subscription = session.execute(select_subscription_query).first()
    if cursor_subscription is None:
        raise SystemError("test: test_should_update_type something went wrong")
    result_subscription = deepcopy(cursor_subscription)
    assert result_user[0] == account.id
    assert result_user[1] == account.external_id
    assert result_user[2] == account.created_at
    assert result_user[3] is None
    assert result_subscription[1] == account.id
    assert result_subscription[2] == AccountType.POST_PAID_MONTH
    assert result_subscription[4] is None
    delete_account(session, account.id)
