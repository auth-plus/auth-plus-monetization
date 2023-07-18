from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Float, MetaData, String, Table, insert, select
from sqlalchemy.orm import Session

from src.config.database import engine
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
    Column("event_id", SQLUUID, nullable=False),
    Column("created_at", TIMESTAMP),
)


class LedgerRepository(CreatingTransaction, ReadingTransaction):
    def create_transaction(
        self, account_id: UUID, amount: float, description: str, event_id=None | UUID
    ) -> Transaction:
        with Session(engine) as session:
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
            row = session.execute(insert_line).first()
            session.commit()
            if row is None:
                raise Exception("somethinf wrong happen")
            (id, created_at) = deepcopy(row)
            return Transaction(
                id, account_id, amount, description, event_id, created_at
            )

    def by_account_id(
        self, account_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> List[Transaction]:
        with Session(engine) as session:
            query = select(ledger_table).where(ledger_table.c.id == account_id)
            cursor = session.execute(query).all()
            if cursor is None:
                return []
            else:
                tuples = deepcopy(cursor)
                transaction_list: List[Transaction] = list(
                    map(
                        lambda t: Transaction(
                            t.id,
                            account_id,
                            t.amount,
                            t.description,
                            t.event_id,
                            t.created_at,
                        ),
                        tuples,
                    )
                )
                return transaction_list
