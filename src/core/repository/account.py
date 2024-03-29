from copy import deepcopy
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, Column, Enum, MetaData, Table, insert, select, update
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.reading_account import (
    AccountNotFoundException,
    ReadingAccount,
)
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
    def __init__(self, session: Session):
        self.session = session

    def create(self, external_id: UUID, type_: AccountType) -> Account:
        insert_line = (
            insert(account_table)
            .values(external_id=external_id, type=type_)
            .returning(account_table.c.id, account_table.c.created_at)
        )
        row = self.session.execute(insert_line).first()
        self.session.commit()
        if row is None:
            raise SystemError("Something on database did not return")
        (id_, created_at) = deepcopy(row)
        return Account(id_, external_id, type_, True, created_at)

    def by_id(self, account_id: UUID) -> Account:
        query = select(account_table).where(account_table.c.id == account_id).limit(1)
        row = self.session.execute(query).first()
        if row is None:
            raise AccountNotFoundException("account not found")
        (id_, external_id, type_, is_enable, created_at) = deepcopy(row)
        return Account(id_, external_id, type_, is_enable, created_at)

    def by_external_id(self, external_id: UUID) -> Account:
        query = (
            select(account_table)
            .where(account_table.c.external_id == external_id)
            .limit(1)
        )
        row = self.session.execute(query).first()
        if row is None:
            raise AccountNotFoundException("account not found")
        (id_, external_id, type_, is_enable, created_at) = deepcopy(row)
        return Account(id_, external_id, type_, is_enable, created_at)

    def change_type(self, account_id: UUID, type_: AccountType) -> None:
        query = (
            update(account_table)
            .values(type=type_)
            .where(account_table.c.id == account_id)
        )
        self.session.execute(query)
        self.session.commit()
