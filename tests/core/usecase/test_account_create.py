from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType, Subscription
from src.core.repository.account import AccountRepository
from src.core.usecase.account_create import AccountCreate
from src.core.usecase.driven.creating_account import CreatingAccount


def test_should_create(session: Session):
    id_ = uuid4()
    external_id = uuid4()
    type_ = AccountType.PRE_PAID
    subscription = Subscription(uuid4(), type_, datetime.now(), None)
    # mock
    creating_account: CreatingAccount = AccountRepository(session)
    creating_account.create = MagicMock(
        return_value=Account(id_, subscription, external_id, datetime.now(), None)
    )
    # usecase
    usecase = AccountCreate(creating_account)
    result = usecase.create(external_id, type_)
    # assert
    assert result.id == id_
    assert result.external_id == external_id
    assert result.subscription.type.value == type_.value
    assert isinstance(result.created_at, datetime)
    creating_account.create.assert_called_once_with(external_id, type_)
