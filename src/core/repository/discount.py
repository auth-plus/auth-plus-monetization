from copy import deepcopy
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Float,
    MetaData,
    String,
    Table,
    insert,
    select,
)
from sqlalchemy.orm import Session

from src.config.database import engine
from src.core.entity.discount import Discount, DiscountType
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.reading_discount import ReadingDiscount

metadata_obj = MetaData()

discount_table = Table(
    "discount",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("account_id", SQLUUID, nullable=False),
    Column("reason", String(255), nullable=False),
    Column("is_enable", Boolean),
    Column("amount", Float, nullable=False),
    Column("type", Enum(DiscountType), nullable=False),
    Column("created_at", TIMESTAMP),
)


class DiscountRepository(CreatingDiscount, ReadingDiscount):
    def create_discount(
        self, account_id: UUID, reason: str, amount: float, type: DiscountType
    ) -> Discount:
        with Session(engine) as session:
            insert_line = (
                insert(discount_table)
                .values(
                    account_id=account_id, reason=reason, amount=amount, type=type.name
                )
                .returning(discount_table.c.id, discount_table.c.created_at)
            )
            row = session.execute(insert_line).first()
            session.commit()
            if row is None:
                raise Exception("somethin wrong happen when inserting")
            (id, created_at) = deepcopy(row)
            return Discount(id, account_id, reason, amount, type, True, created_at)

    def by_account_id(self, account_id: UUID) -> Discount:
        with Session(engine) as session:
            query = (
                select(discount_table).where(discount_table.c.id == account_id).limit(1)
            )
            row = session.execute(query).first()
            if row is None:
                raise Exception("discount not found")
            (id, account_id, reason, type, amount, is_enable, created_at) = deepcopy(
                row
            )
            return Discount(id, account_id, reason, amount, type, is_enable, created_at)
