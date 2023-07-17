from copy import deepcopy
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.account import AccountType
from src.core.repository.account import AccountRepository, account_table


def test_should_create():
    external_id = uuid4()
    type = AccountType.PRE_PAID

    repository = AccountRepository()
    result = repository.create(external_id, type)
    assert isinstance(result.id, UUID)
    assert result.external_id == external_id
    assert result.type == type
    assert result.is_enable
    assert isinstance(result.created_at, datetime)
    with Session(engine) as session:
        delete_query = delete(account_table).where(account_table.c.id == result.id)
        session.execute(delete_query)
        session.commit()


def test_should_select_by_id():
    external_id = uuid4()
    type = AccountType.PRE_PAID
    with Session(engine) as session:
        insert_line = (
            insert(account_table)
            .values(external_id=external_id, type=type.name)
            .returning(account_table.c.id, account_table.c.created_at)
        )
        cursor = session.execute(insert_line)
        (id, created_at) = deepcopy(cursor.first())
        session.commit()
        repository = AccountRepository()
        result = repository.by_id(id)
        assert result.id == id
        assert result.external_id == external_id
        assert result.type == type.name
        assert result.is_enable
        assert result.created_at == created_at
        delete_query = delete(account_table).where(account_table.c.id == id)
        session.execute(delete_query)
        session.commit()


def test_should_update_type():
    external_id = uuid4()
    type = AccountType.PRE_PAID
    with Session(engine) as session:
        insert_line = (
            insert(account_table)
            .values(external_id=external_id, type=type.name)
            .returning(account_table.c.id, account_table.c.created_at)
        )
        cursor = session.execute(insert_line)
        (id, created_at) = deepcopy(cursor.first())
        session.commit()
        repository = AccountRepository()
        repository.change_type(id, AccountType.POST_PAID)
        select_query = select(account_table).where(account_table.c.id == id).limit(1)
        cursor = session.execute(select_query)
        result = deepcopy(cursor.first())
        assert result[0] == id
        assert result[1] == external_id
        assert result[2] == AccountType.POST_PAID.name
        assert result[3]
        assert result[4] == created_at
        delete_query = delete(account_table).where(account_table.c.id == id)
        session.execute(delete_query)
        session.commit()
