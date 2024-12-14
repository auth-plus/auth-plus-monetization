from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.repository.account import AccountRepository
from src.core.usecase.account_create import AccountCreate
from src.core.usecase.driven.creating_account import CreatingAccount


def test_should_create(session: Session):
    id_ = uuid4()
    external_id = uuid4()
    type_ = AccountType.PRE_PAID
    # mock
    creating_account: CreatingAccount = AccountRepository(session)
    creating_account.create = MagicMock(
        return_value=Account(id_, external_id, type_, datetime.now(), None)
    )
    # usecase
    usecase = AccountCreate(creating_account)
    result = usecase.create(external_id, type_)
    # assert
    assert result.id == id_
    assert result.external_id == external_id
    assert result.type == type_
    assert isinstance(result.created_at, datetime)
    creating_account.create.assert_called_once_with(external_id, type_)
