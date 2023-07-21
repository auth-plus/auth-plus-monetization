from copy import deepcopy
from decimal import Decimal
from uuid import UUID

from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from src.core.entity.account import Account, AccountType
from src.core.entity.discount import Discount, DiscountType
from src.core.entity.event import Event, EventType
from src.core.entity.transaction import Transaction
from src.core.repository.account import account_table
from src.core.repository.discount import discount_table
from src.core.repository.event import event_table
from src.core.repository.ledger import ledger_table


# ACCOUNT
def create_account(session: Session, external_id: UUID, type: AccountType):
    insert_line = (
        insert(account_table)
        .values(external_id=external_id, type=type)
        .returning(account_table.c.id, account_table.c.created_at)
    )
    cursor = session.execute(insert_line)
    (id, created_at) = deepcopy(cursor.first())
    session.commit()
    return Account(id, external_id, type, True, created_at)


def delete_account(session: Session, id: UUID):
    delete_query = delete(account_table).where(account_table.c.id == id)
    session.execute(delete_query)
    session.commit()


# DISCOUNT
def create_discount(
    session: Session, account_id: UUID, reason: str, amount: float, type: DiscountType
):
    insert_line = (
        insert(discount_table)
        .values(account_id=account_id, reason=reason, amount=amount, type=type)
        .returning(
            discount_table.c.id, discount_table.c.is_enable, discount_table.c.created_at
        )
    )
    cursor = session.execute(insert_line)
    (id, is_enable, created_at) = deepcopy(cursor.first())
    session.commit()
    return Discount(id, account_id, reason, amount, type, is_enable, created_at)


def delete_discount(session: Session, id: UUID):
    delete_query = delete(discount_table).where(discount_table.c.id == id)
    session.execute(delete_query)
    session.commit()


# EVENT
def create_event(session: Session, type: EventType, price: float):
    insert_line = (
        insert(event_table)
        .values(type=type, price=Decimal(price))
        .returning(event_table.c.id, event_table.c.created_at)
    )
    cursor = session.execute(insert_line)
    (id, created_at) = deepcopy(cursor.first())
    session.commit()
    return Event(id, type, price, created_at)


def delete_event(session: Session, id: UUID):
    delete_query = delete(event_table).where(event_table.c.id == id)
    session.execute(delete_query)
    session.commit()


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
            event_id=event_id,
        )
        .returning(ledger_table.c.id, ledger_table.c.created_at)
    )
    cursor = session.execute(insert_line)
    (id, created_at) = deepcopy(cursor.first())
    session.commit()
    return Transaction(id, account_id, amount, description, event_id, created_at)


def delete_transaction(session: Session, id: UUID):
    delete_query = delete(ledger_table).where(ledger_table.c.id == id)
    session.execute(delete_query)
    session.commit()
