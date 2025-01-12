import datetime
from copy import deepcopy
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.discount import Discount, DiscountType
from src.core.entity.event import Event, EventType
from src.core.entity.transaction import Transaction
from src.core.repository.account import account_table, subscription_table
from src.core.repository.discount import discount_table
from src.core.repository.ledger import ledger_table
from src.core.repository.price import event_table


# ACCOUNT
def create_account(
    session: Session,
    external_id: UUID,
    type_: AccountType,
    created_at: Optional[datetime.datetime] = None,
):
    account_insert_line = (
        insert(account_table)
        .values(
            external_id=external_id,
            type=type_,
            created_at=(
                created_at if created_at is not None else datetime.datetime.now()
            ),
        )
        .returning(
            account_table.c.id, account_table.c.created_at, account_table.c.deleted_at
        )
    )
    cursor_user = session.execute(account_insert_line).first()
    session.commit()
    if cursor_user is None:
        raise SystemError("test: create_account something went wrong")
    (id_, created_at_, deleted_at_) = deepcopy(cursor_user)
    subscription_insert_line = insert(subscription_table).values(
        account_id=id_, type=type_
    )
    cursor_subscription = session.execute(subscription_insert_line)
    if cursor_subscription is None:
        raise SystemError("test: create_account something went wrong")
    session.commit()
    return Account(id_, external_id, type_, created_at_, deleted_at_)


def delete_account(session: Session, id_: UUID):
    subscription_delete_query = delete(subscription_table).where(
        subscription_table.c.account_id == id_
    )
    session.execute(subscription_delete_query)
    account_delete_query = delete(account_table).where(account_table.c.id == id_)
    session.execute(account_delete_query)
    session.commit()


# DISCOUNT
def create_discount(
    session: Session, account_id: UUID, reason: str, amount: float, type_: DiscountType
):
    insert_line = (
        insert(discount_table)
        .values(account_id=account_id, reason=reason, amount=amount, type=type_)
        .returning(
            discount_table.c.id,
            discount_table.c.deleted_at,
            discount_table.c.created_at,
        )
    )
    cursor = session.execute(insert_line).first()
    if cursor is None:
        raise SystemError("test: create_discount something went wrong")
    (id_, deleted_at, created_at) = deepcopy(cursor)
    session.commit()
    return Discount(id_, account_id, reason, amount, type_, created_at, deleted_at)


def delete_discount(session: Session, id_: UUID):
    delete_query = delete(discount_table).where(discount_table.c.id == id_)
    session.execute(delete_query)
    session.commit()


# EVENT
def get_event(session: Session):
    query = (
        select(event_table)
        .where(event_table.c.event == EventType.EMAIL_AUTH_FACTOR_SENT)
        .limit(1)
    )
    cursor = session.execute(query).first()
    session.commit()
    if cursor is None:
        raise SystemError("test: create_event something went wrong")
    (id_, event_, value_, created_at, deleted_at) = deepcopy(cursor)
    return Event(id_, event_, value_, created_at)


# Ledger
def create_transaction(
    session: Session, account_id: UUID, amount: float, description: str, event_id: UUID
):
    insert_line = (
        insert(ledger_table)
        .values(
            account_id=account_id,
            amount=amount,
            description=description,
            price_id=event_id,
        )
        .returning(ledger_table.c.id, ledger_table.c.created_at)
    )
    cursor = session.execute(insert_line).first()
    if cursor is None:
        raise SystemError("test: create_transaction something went wrong")
    (id_, created_at) = deepcopy(cursor)
    session.commit()
    return Transaction(id_, account_id, amount, description, event_id, created_at)


def delete_transaction(session: Session, id_: UUID):
    delete_query = delete(ledger_table).where(ledger_table.c.id == id_)
    session.execute(delete_query)
    session.commit()
