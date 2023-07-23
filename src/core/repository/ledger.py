from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Float, MetaData, String, Table, insert, select
from sqlalchemy.orm import Session

from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_transaction import ReadingTransaction

metadata_obj = MetaData()

ledger_table = Table(
    "ledger",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("account_id", SQLUUID, nullable=False),
    Column("amount", Float, nullable=False),
    Column("description", String(255), nullable=False),
    Column("event_id", SQLUUID, nullable=True),
    Column("created_at", TIMESTAMP),
)


class LedgerRepository(CreatingTransaction, ReadingTransaction):
    def __init__(self, session: Session):
        self.session = session

    def create_transaction(
        self, account_id: UUID, amount: float, description: str, event_id=None | UUID
    ) -> Transaction:
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
        row = self.session.execute(insert_line).first()
        self.session.commit()
        if row is None:
            raise SystemError("Something on database did not return")
        (id_, created_at) = deepcopy(row)
        return Transaction(id_, account_id, amount, description, event_id, created_at)

    def by_account_id(
        self, account_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> List[Transaction]:
        query = select(ledger_table).where(ledger_table.c.account_id == account_id)
        cursor = self.session.execute(query).all()
        if cursor is None:
            return []
        else:
            transaction_list = deepcopy(cursor)
            return list(
                map(
                    lambda t: Transaction(
                        t.id,
                        account_id,
                        t.amount,
                        t.description,
                        t.event_id,
                        t.created_at,
                    ),
                    transaction_list,
                )
            )
