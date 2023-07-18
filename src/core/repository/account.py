from copy import deepcopy
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, Column, Enum, MetaData, Table, insert, select, update
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.reading_account import ReadingAccount
from src.core.usecase.driven.update_account import UpdateAccount

metadata_obj = MetaData()

account_table = Table(
    "account",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("external_id", SQLUUID, nullable=False),
    Column("type", Enum(AccountType), nullable=False),
    Column("is_enable", Boolean),
    Column("created_at", TIMESTAMP),
)


class AccountRepository(CreatingAccount, ReadingAccount, UpdateAccount):
    def create(self, external_id: UUID, type: AccountType) -> Account:
        with Session(engine) as session:
            insert_line = (
                insert(account_table)
                .values(external_id=external_id, type=type.name)
                .returning(account_table.c.id, account_table.c.created_at)
            )
            row = session.execute(insert_line).first()
            session.commit()
            if row is None:
                raise Exception("somethinf wrong happen")
            (id, created_at) = deepcopy(row)
            return Account(id, external_id, type, True, created_at)

    def by_id(self, account_id: UUID) -> Account:
        with Session(engine) as session:
            query = (
                select(account_table).where(account_table.c.id == account_id).limit(1)
            )
            row = session.execute(query).first()
            if row is None:
                raise Exception("account not found")
            (id, external_id, type, is_enable, created_at) = deepcopy(row)
            return Account(id, external_id, type, is_enable, created_at)

    def by_external_id(self, external_id: UUID) -> Account:
        with Session(engine) as session:
            query = (
                select(account_table)
                .where(account_table.c.external_id == external_id)
                .limit(1)
            )
            row = session.execute(query).first()
            if row is None:
                raise Exception("account not found")
            (id, external_id, type, is_enable, created_at) = deepcopy(row)
            return Account(id, external_id, type, is_enable, created_at)

    def change_type(self, account_id: UUID, type: AccountType) -> None:
        with Session(engine) as session:
            query = (
                update(account_table)
                .values(type=type.name)
                .where(account_table.c.id == account_id)
            )
            session.execute(query)
            session.commit()
