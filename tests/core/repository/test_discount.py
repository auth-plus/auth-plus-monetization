from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import AccountType
from src.core.entity.discount import DiscountType
from src.core.repository.discount import DiscountRepository
from tests.factory.helpers import (
    create_account,
    create_discount,
    delete_account,
    delete_discount,
)


def test_should_create(session: Session):
    reason = "reason"
    amount = 111.5
    type_ = DiscountType.PERCENTAGE
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    repository = DiscountRepository(session)
    result = repository.create_discount(account.id, reason, amount, type_)
    assert isinstance(result.id, UUID)
    assert result.account_id == account.id
    assert result.reason == reason
    assert result.is_enable
    assert result.amount == amount
    assert result.type == type_
    assert isinstance(result.created_at, datetime)
    delete_discount(session, result.id)
    delete_account(session, account.id)


def test_should_select_by_account_id(session: Session):
    account = create_account(session, uuid4(), AccountType.PRE_PAID)
    discount = create_discount(
        session, account.id, "reason", 111.5, DiscountType.ABSOLUTE
    )
    repository = DiscountRepository(session)
    result = repository.by_account_id(account.id)
    assert result.id == discount.id
    assert result.account_id == account.id
    assert result.reason == discount.reason
    assert result.is_enable
    assert result.amount == discount.amount
    assert result.type == discount.type
    assert result.created_at == discount.created_at
    delete_discount(session, result.id)
    delete_account(session, account.id)
