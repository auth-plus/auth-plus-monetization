from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import (
    TIMESTAMP,
)
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import (
    Column,
    Enum,
    MetaData,
    Table,
    and_,
    extract,
    insert,
    or_,
    select,
    update,
)
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType, Subscription
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
            .values(external_id=external_id)
            .returning(account_table.c.id, account_table.c.created_at)
        )
        account_row = self.session.execute(insert_line).first()
        if account_row is None:
            raise SystemError("Something on database did not return")
        (account_id, account_created_at) = deepcopy(account_row)
        query_subscription_insert = (
            insert(subscription_table)
            .values(account_id=account_id, type=type_)
            .returning(subscription_table.c.id, subscription_table.c.created_at)
        )
        subscription_row = self.session.execute(query_subscription_insert)
        if subscription_row is None:
            raise SystemError("Something on database did not return")
        (subscription_id, subscription_created_at) = deepcopy(account_row)
        self.session.commit()
        subscription = Subscription(
            subscription_id, type_, subscription_created_at, None
        )
        return Account(account_id, subscription, external_id, account_created_at, None)

    def by_id(self, account_id: UUID) -> Account:
        query = (
            select(account_table, subscription_table)
            .select_from(account_table)
            .join(
                subscription_table,
                account_table.c.id == subscription_table.c.account_id,
            )
            .where(
                account_table.c.id == account_id,
                subscription_table.c.deleted_at.is_(None),
            )
            .limit(1)
        )
        row = self.session.execute(query).first()
        self.session.commit()
        if row is None:
            raise AccountNotFoundException("account not found")
        (
            account_id,
            external_id,
            account_created_at,
            account_deleted_at,
            subscription_id,
            _,
            type,
            subscription_created_at,
            subscription_deleted_at,
        ) = deepcopy(row)
        subscription = Subscription(
            subscription_id, type, subscription_created_at, subscription_deleted_at
        )
        return Account(
            account_id,
            subscription,
            external_id,
            account_created_at,
            account_deleted_at,
        )

    def by_external_id(self, external_id: UUID) -> Account:
        query = (
            select(account_table, subscription_table)
            .select_from(account_table)
            .join(
                subscription_table,
                account_table.c.id == subscription_table.c.account_id,
            )
            .where(
                account_table.c.external_id == external_id,
                subscription_table.c.deleted_at.is_(None),
            )
            .limit(1)
        )
        row = self.session.execute(query).first()
        if row is None:
            raise AccountNotFoundException("account not found")
        (
            account_id,
            external_id,
            account_created_at,
            account_deleted_at,
            subscription_id,
            _,
            type,
            subscription_created_at,
            subscription_deleted_at,
        ) = deepcopy(row)
        subscription = Subscription(
            subscription_id, type, subscription_created_at, subscription_deleted_at
        )
        return Account(
            account_id,
            subscription,
            external_id,
            account_created_at,
            account_deleted_at,
        )

    def change_type(self, account_id_: UUID, type_: AccountType) -> None:
        query_subscription_delete = (
            update(subscription_table)
            .values(deleted_at=datetime.now())
            .where(subscription_table.c.account_id == account_id_)
        )
        query_subscription_insert = insert(subscription_table).values(
            account_id=account_id_, type=type_
        )
        self.session.execute(query_subscription_delete)
        self.session.execute(query_subscription_insert)
        self.session.commit()

    def by_subscription_period(self) -> List[Account]:
        today = datetime.today()
        annual_criteria = and_(
            subscription_table.c.type == AccountType.POST_PAID_ANNUAL,
            extract("month", subscription_table.c.created_at) == today.month,
            extract("day", subscription_table.c.created_at) == today.day,
        )

        monthly_criteria = and_(
            subscription_table.c.type == AccountType.POST_PAID_MONTH,
            extract("day", subscription_table.c.created_at) == today.day,
        )

        semester_criteria = and_(
            subscription_table.c.type == AccountType.POST_PAID_SEMESTER,
            extract("day", subscription_table.c.created_at) == today.day,
            or_(
                extract("month", subscription_table.c.created_at) == today.month,
                extract("month", subscription_table.c.created_at)
                == ((today.month - 7) % 12 + 1),
            ),
        )

        # Combine all with a filter to ensure we don't pick up records created TODAY
        query = self.session.query(subscription_table).filter(
            subscription_table.c.created_at < today,
            subscription_table.c.deleted_at.is_(None),
            or_(
                annual_criteria,
                semester_criteria,
                monthly_criteria,
            ),
        )
        subscription_list = query.all()
        query_user_select = (
            select(account_table)
            .select_from(account_table)
            .where(
                account_table.c.id.in_(
                    map(lambda subs: subs.account_id, subscription_list)
                )
            )
        )
        users_row = self.session.execute(query_user_select).all()
        user_list = list(map(lambda u: deepcopy(u), users_row))
        resp = []
        for account in user_list:
            (account_id, external_id, account_created_at, account_deleted_at) = (
                deepcopy(account)
            )
            [subscription] = filter(
                lambda s: s.account_id == account_id, subscription_list
            )
            acc = Account(
                account.id,
                subscription,
                external_id,
                account_created_at,
                account_deleted_at,
            )
            resp.append(acc)
        return resp
