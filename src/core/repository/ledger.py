from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Float, MetaData, String, Table, insert, select, update
from sqlalchemy.orm import Session

from src.core.entity.transaction import Transaction
from src.core.usecase.driven.creating_transaction import CreatingTransaction
from src.core.usecase.driven.reading_transaction import ReadingTransaction
from src.core.usecase.driven.update_transaction import UpdatingTransaction

metadata_obj = MetaData()

ledger_table = Table(
    "ledger",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("account_id", SQLUUID, nullable=False),
    Column("amount", Float, nullable=False),
    Column("description", String(255), nullable=False),
    Column("price_id", SQLUUID),
    Column("charge_id", SQLUUID),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP),
)


class LedgerRepository(CreatingTransaction, ReadingTransaction, UpdatingTransaction):
    def __init__(self, session: Session):
        self.session = session

    def create_transaction(
        self, account_id: UUID, amount: float, description: str, price_id=None | UUID
    ) -> Transaction:
        insert_line = (
            insert(ledger_table)
            .values(
                account_id=account_id,
                amount=amount,
                description=description,
                price_id=price_id,
            )
            .returning(ledger_table.c.id, ledger_table.c.created_at)
        )
        row = self.session.execute(insert_line).first()
        self.session.commit()
        if row is None:
            raise SystemError("Something on database did not return")
        (id_, created_at) = deepcopy(row)
        return Transaction(id_, account_id, amount, description, price_id, created_at)

    def by_account_id(
        self, account_id: UUID, date_start: datetime, date_end=datetime.now()
    ) -> List[Transaction]:
        query = select(ledger_table).where(ledger_table.c.account_id == account_id)
        cursor = self.session.execute(query).all()
        self.session.commit()
        if cursor is None:
            return []
        else:
            transaction_list = deepcopy(cursor)
            return list(
                map(
                    lambda t: Transaction(
                        t.id,
                        t.account_id,
                        t.amount,
                        t.description,
                        t.price_id,
                        t.created_at,
                    ),
                    transaction_list,
                )
            )

    def add_charge(self, account_id: UUID, charge_id: UUID) -> None:
        query = (
            update(ledger_table)
            .values(charge_id=charge_id)
            .where(
                ledger_table.c.account_id == account_id,
                ledger_table.c.charge_id.__eq__(None),
            )
        )
        self.session.execute(query)
        self.session.commit()
