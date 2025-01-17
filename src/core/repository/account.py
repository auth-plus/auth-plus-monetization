import datetime
from copy import deepcopy
from typing import List
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Enum, MetaData, Table, extract, insert, select, update
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.usecase.driven.creating_account import CreatingAccount
from src.core.usecase.driven.reading_account import (
    AccountNotFoundException,
    ReadingAccount,
)
from src.core.usecase.driven.update_account import UpdatingAccount

metadata_obj = MetaData()

account_table = Table(
    "account",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("external_id", SQLUUID, nullable=False),
    Column("type", Enum(AccountType), nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP),
)

subscription_table = Table(
    "subscription",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("account_id", SQLUUID, nullable=False),
    Column("type", Enum(AccountType), nullable=False),
    Column("created_at", TIMESTAMP),
    Column("deleted_at", TIMESTAMP),
)


class AccountRepository(CreatingAccount, ReadingAccount, UpdatingAccount):
    def __init__(self, session: Session):
        self.session = session

    def create(self, external_id: UUID, type_: AccountType) -> Account:
        insert_line = (
            insert(account_table)
            .values(external_id=external_id, type=type_)
            .returning(account_table.c.id, account_table.c.created_at)
        )
        row = self.session.execute(insert_line).first()
        if row is None:
            raise SystemError("Something on database did not return")
        (id_, created_at) = deepcopy(row)
        query_subscription_insert = insert(subscription_table).values(
            account_id=id_, type=type_
        )
        self.session.execute(query_subscription_insert)
        self.session.commit()
        return Account(id_, external_id, type_, created_at, None)

    def by_id(self, account_id: UUID) -> Account:
        query = select(account_table).where(account_table.c.id == account_id).limit(1)
        row = self.session.execute(query).first()
        self.session.commit()
        if row is None:
            raise AccountNotFoundException("account not found")
        (id_, external_id, type_, created_at, deleted_at) = deepcopy(row)
        return Account(id_, external_id, type_, created_at, deleted_at)

    def by_external_id(self, external_id: UUID) -> Account:
        query = (
            select(account_table)
            .where(account_table.c.external_id == external_id)
            .limit(1)
        )
        row = self.session.execute(query).first()
        if row is None:
            raise AccountNotFoundException("account not found")
        (id_, external_id, type_, created_at, deleted_at) = deepcopy(row)
        return Account(id_, external_id, type_, created_at, deleted_at)

    def change_type(self, account_id_: UUID, type_: AccountType) -> None:
        query_user_update = (
            update(account_table)
            .values(type=type_)
            .where(account_table.c.id == account_id_)
        )
        query_subscription_delete = (
            update(subscription_table)
            .values(deleted_at=datetime.datetime.now())
            .where(subscription_table.c.account_id == account_id_)
        )
        query_subscription_insert = insert(subscription_table).values(
            account_id=account_id_, type=type_
        )
        self.session.execute(query_user_update)
        self.session.execute(query_subscription_delete)
        self.session.execute(query_subscription_insert)
        self.session.commit()

    def by_subscription_period(self) -> List[Account]:
        today = datetime.datetime.today()
        query_subscription = (
            select(account_table)
            .join(
                subscription_table,
                account_table.c.id == subscription_table.c.account_id,
            )
            .where(
                extract("day", subscription_table.c.created_at) == today.day,
                subscription_table.c.deleted_at.__eq__(None),
            )
        )
        rows = self.session.execute(query_subscription).all()
        if len(rows) == 0:
            return []
        return list(
            map(
                lambda row: Account(
                    row.id, row.external_id, row.type, row.created_at, row.deleted_at
                ),
                rows,
            )
        )
