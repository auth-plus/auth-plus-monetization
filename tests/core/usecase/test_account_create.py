from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from src.core.entity.account import Account, AccountType
from src.core.repository.account import AccountRepository
from src.core.usecase.account_create import AccountCreate
from src.core.usecase.driven.creating_account import CreatingAccount
from sqlalchemy.orm import Session


def test_should_create(session: Session):
    id = uuid4()
    external_id = uuid4()
    type = AccountType.PRE_PAID
    # mock
    creating_account: CreatingAccount = AccountRepository(session)
    creating_account.create = MagicMock(
        return_value=Account(id, external_id, type, True, datetime.now())
    )
    # usecase
    usecase = AccountCreate(creating_account)
    result = usecase.create(external_id, type)
    # assert
    assert result.id == id
    assert result.external_id == external_id
    assert result.type == type
    assert result.is_enable
    assert isinstance(result.created_at, datetime)
    creating_account.create.assert_called_once_with(external_id, type)
