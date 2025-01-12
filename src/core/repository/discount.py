from copy import deepcopy
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, Enum, Float, MetaData, String, Table, insert, select
from sqlalchemy.orm import Session

from src.core.entity.discount import Discount, DiscountType
from src.core.usecase.driven.creating_discount import CreatingDiscount
from src.core.usecase.driven.reading_discount import (
    DiscountNotFoundException,
    ReadingDiscount,
)

metadata_obj = MetaData()

discount_table = Table(
    "discount",
    metadata_obj,
    Column("id", SQLUUID, nullable=False),
    Column("account_id", SQLUUID, nullable=False),
    Column("reason", String(255), nullable=False),
    Column("amount", Float, nullable=False),
    Column("type", Enum(DiscountType), nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("deleted_at", TIMESTAMP),
)


class DiscountRepository(CreatingDiscount, ReadingDiscount):
    def __init__(self, session: Session):
        self.session = session

    def create_discount(
        self, account_id: UUID, reason: str, amount: float, type_: DiscountType
    ) -> Discount:
        insert_line = (
            insert(discount_table)
            .values(account_id=account_id, reason=reason, amount=amount, type=type_)
            .returning(
                discount_table.c.id,
                discount_table.c.created_at,
                discount_table.c.deleted_at,
            )
        )
        row = self.session.execute(insert_line).first()
        self.session.commit()
        if row is None:
            raise SystemError("Something on database did not return")
        (id_, created_at, deleted_at) = deepcopy(row)
        return Discount(id_, account_id, reason, amount, type_, created_at, deleted_at)

    def by_account_id(self, account_id: UUID) -> Discount:
        query = (
            select(discount_table)
            .where(
                discount_table.c.account_id == account_id,
                discount_table.c.deleted_at.__eq__(None),
            )
            .limit(1)
            .order_by(discount_table.c.created_at.desc())
        )
        row = self.session.execute(query).first()
        if row is None:
            raise DiscountNotFoundException("discount not found")
        (id_, account_id, reason, amount, type_, created_at, deleted_at) = deepcopy(row)
        return Discount(id_, account_id, reason, amount, type_, created_at, deleted_at)
